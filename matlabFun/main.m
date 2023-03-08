% 航迹生成
clc; clear; close all;

parameter.xMax = 5000; parameter.xMin = -5000; % 场景边界 （目标出生点范围）
parameter.vMax = 10; parameter.vMin = -10; % 速度边界
parameter.aMax = 0.1; parameter.aMin = -0.1; % 加速度边界

parameter.dimX = 6; % 状态维度

K = 100; % 观测步长
T = 1; % 观测周期

RadarPos = [5000, -5000; 0, 0; -5000, 5000]; % 三部雷达位置
RadarNums = 3; % 雷达数量
radarT = [3,2,4]; % 雷达量测周期


dataSize = 10000; % batch数据大小
genBatchData(dataSize, RadarNums, parameter, K, RadarPos, radarT, T);