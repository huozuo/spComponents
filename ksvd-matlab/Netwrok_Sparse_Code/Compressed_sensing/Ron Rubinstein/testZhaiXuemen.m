clc;
clear;
close all;

global GSparseInvParam;
load GSparseInvParam;

GSparseInvParam.sizeAtom = 400;              % ԭ�Ӵ�С
GSparseInvParam.nAtom = 200;                % ԭ�Ӹ���
GSparseInvParam.trainCutInterval = 1;       % ѵ��ʱ�����и���
GSparseInvParam.trainSparsity = 3;
GSparseInvParam.trainIterNum = 20;         % ѵ����������
GSparseInvParam.isShowRebuildResult = 0;
GSparseInvParam.trainFiltCoef = 1;        % ѵ�������˲��̶�
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

datas = load(Name);                % ѵ������·��
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