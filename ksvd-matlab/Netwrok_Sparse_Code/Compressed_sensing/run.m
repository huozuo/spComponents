clc;
clear;
close all;

global GSparseInvParam;
load GSparseInvParam;

GSparseInvParam.sizeAtom = 10;              % 原子大小
GSparseInvParam.nAtom = 200;                % 原子个数
GSparseInvParam.trainCutInterval = 1;       % 训练时样本切割间隔
GSparseInvParam.trainSparsity = 3;
GSparseInvParam.trainIterNum = 20;         % 训练迭代次数
GSparseInvParam.isShowRebuildResult = 0;
GSparseInvParam.trainFiltCoef = 1;        % 训练样本滤波程度
GSparseInvParam.isShowIterInfo = 0;
id = 1;

datas = load('Sample_yago_10.txt');                % 训练样本路径
datas = datas';

params.data = datas;
params.Tdata = GSparseInvParam.trainSparsity;
params.dictsize = GSparseInvParam.nAtom; 
params.iternum = GSparseInvParam.trainIterNum;
params.memusage = 'high';

[dic] = ksvd(params, GSparseInvParam.isShowIterInfo);

dlmwrite(sprintf('dic_Sample.txt'), dic, ' ');

G = dic'*dic;
Gamma = omp(dic'* datas, G, 3);
Gamma = full(Gamma);
dlmwrite(sprintf('coef_Sample.txt'), Gamma, ' ');        
% stpTrainDictionary