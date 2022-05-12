clc;
clear;
close all;

global GSparseInvParam;
load GSparseInvParam;

GSparseInvParam.sizeAtom = 10;              % ԭ�Ӵ�С
GSparseInvParam.nAtom = 200;                % ԭ�Ӹ���
GSparseInvParam.trainCutInterval = 1;       % ѵ��ʱ�����и���
GSparseInvParam.trainSparsity = 3;
GSparseInvParam.trainIterNum = 20;         % ѵ����������
GSparseInvParam.isShowRebuildResult = 0;
GSparseInvParam.trainFiltCoef = 1;        % ѵ�������˲��̶�
GSparseInvParam.isShowIterInfo = 0;
id = 1;

datas = load('Sample_yago_10.txt');                % ѵ������·��
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