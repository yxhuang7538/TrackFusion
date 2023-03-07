trajectory = genOneTraj(K, T, parameter); % 生成轨迹

figure;
meas1 = genOneMeas(trajectory, K, T, radarT(1), parameter, RadarPos(1, :)'); % 生成量测
meas2 = genOneMeas(trajectory, K, T, radarT(2), parameter, RadarPos(2, :)'); % 生成量测
plot(1 : K, meas1(1, :), "b--o"); hold on; % 插值前
plot(1 : K, meas2(1, :), "r--*"); hold on;
meas1 = interpOneMea(meas1, K, T, radarT(1));
meas2 = interpOneMea(meas2, K, T, radarT(2));
figure;
plot(1 : K, meas1(1, :), "b--o"); hold on; % 插值后
plot(1 : K, meas2(1, :), "r--*"); hold on; % 插值后