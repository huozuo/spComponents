clc;
clear;
close all;

global GSparseInvParam;
load GSparseInvParam;

GSparseInvParam.sizeAtom = 400;              % 原子大小
GSparseInvParam.nAtom = 200;                % 原子个数
GSparseInvParam.trainCutInterval = 1;       % 训练时样本切割间隔
GSparseInvParam.trainSparsity = 3;
GSparseInvParam.trainIterNum = 20;         % 训练迭代次数
GSparseInvParam.isShowRebuildResult = 0;
GSparseInvParam.trainFiltCoef = 1;        % 训练样本滤波程度
GSparseInvParam.isShowIterInfo = 0;
id = 1;
Name = 'Sample_riot_20.txt';
%Name = 'Sample_rumor_20.txt';
%Name = 'Sample_riot_cascade_20.txt';
%Name = 'Sample_twitter_controled_20.txt';
%Name = 'Sample_out.com-amazon0.txt';
%Name = 'Sample_out.com-youtube7.txt';
%Name = 'Sample_out.com-amazon.txt';
%Name = 'Sample_out.com-youtube.txt';

datas = load(Name);                % 训练样本路径
datas = datas';

params.data = datas;
params.Tdata = GSparseInvParam.trainSparsity;
params.dictsize = GSparseInvParam.nAtom;
params.iternum = GSparseInvParam.trainIterNum;
params.memusage = 'high';

[dic] = ksvd(params, GSparseInvParam.isShowIterInfo);

dlmwrite(sprintf(strcat('dic_', Name), GSparseInvParam.sizeAtom, GSparseInvParam.nAtom, id), dic, ' ');

G = dic'*dic;
Gamma = omp(dic'* datas, G, 3);
Gamma = full(Gamma);
dlmwrite(sprintf(strcat('coef_', Name), GSparseInvParam.sizeAtom, GSparseInvParam.nAtom, id), Gamma, ' ');        
% stpTrainDictionary