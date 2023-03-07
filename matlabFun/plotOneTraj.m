function plotOneTraj(trajectory, meas, RadarPos, radarT, T, K)
% 绘制一条航迹
figure;
plot(trajectory(1, :), trajectory(4, :), "b-o"); hold on;
for ii = 1 : size(meas, 1)
    plot(squeeze(meas(ii, 1, 1:radarT(ii)/T:K)), squeeze(meas(ii, 2, 1:radarT(ii)/T:K)), "--o"); hold on;
end

for ii = 1 : size(RadarPos, 1)
    scatter(RadarPos(ii, 1), RadarPos(ii, 2), 'black', 'filled'); hold on;
end
end

