function meas = interpOneMea(meas, K, T, radarT)
% 插值一个量测
dk = radarT / T;
x = 1 : dk : K;
v = meas(1, 1 : dk : K);
xq = 1 : 1 : K;

meas(1, :) = interp1(x, v, xq, 'spline'); % 插值x

v = meas(2, 1 : dk : K);
meas(2, :) = interp1(x, v, xq, 'spline'); % 插值y

end

