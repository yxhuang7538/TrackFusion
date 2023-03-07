function meas = genOneMeas(trajectory, K, T, radarT, parameter, RadarPos)
% 为每一部雷达生成一条量测

sigmaR=randi([5, 8]); % 距离标准差
sigmaAzimu=deg2rad(0.1 + (0.3 - 0.1) * rand); % 方位标准差 单位度 0.1°~0.3°

dk = radarT / T; % 取样间隔
Z = zeros([parameter.dimX / 3, K]); % 极坐标下的量测
meas = NaN([parameter.dimX / 3, K]); % 转换到直角坐标

for k = 1 : dk : K
    meas(:, k) = trajectory(1 : 3 : parameter.dimX, k) - RadarPos;% + normrnd(0, sigmaR, [2, 1]);
    [Z(1, k), Z(2, k)] = cart2pol(meas(1, k), meas(2, k));
    Z(:, k) = Z(:, k) + [normrnd(0, sigmaAzimu); normrnd(0, sigmaR)];
    [meas(1, k), meas(2, k)] = pol2cart(Z(1, k), Z(2, k));
    meas(:, k) = meas(:, k) + RadarPos;
end

meas = interpOneMea(meas, K, T, radarT); %插值 test的时候注释掉
end

