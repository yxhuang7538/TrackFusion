function trajectory = genOneTraj(K, T, parameter)
% 生成一条真实航迹

xInit = parameter.xMin + (parameter.xMax - parameter.xMin) * rand([parameter.dimX / 3, 1]); % 初始位置
vInit = parameter.vMin + (parameter.vMax - parameter.vMin) * rand([parameter.dimX / 3, 1]); % 初始速度
aInit = parameter.aMin + (parameter.aMax - parameter.aMin) * rand([parameter.dimX / 3, 1]); % 初始速度

trajectory = zeros([parameter.dimX, K]); % 状态值
trajectory(:, 1) = [xInit; vInit; aInit]; % 初始时刻状态值


% CA模型
Fca = [1, T, T^2 / 2, 0, 0, 0; 0, 1, T, 0, 0, 0; 0, 0, 1, 0, 0, 0;
    0, 0, 0, 1, T, T^2 / 2; 0, 0, 0, 0, 1, T; 0, 0, 0, 0, 0, 1];

for k = 2 : K
    trajectory(:, k) = Fca * trajectory(:, k - 1); % 真值
end

end