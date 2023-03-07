function genBatchData(dataSize, RadarNums, parameter, K, RadarPos, radarT, T)
% 生成批量数据
trajectorys = zeros([dataSize, parameter.dimX, K]); % 真值set
meas = zeros([dataSize, RadarNums, parameter.dimX / 3, K]);

for ii = 1 : dataSize
    trajectorys(ii, :, :) = genOneTraj(K, T, parameter);
    for jj = 1 : RadarNums
        meas(ii, jj, :, :) = genOneMeas(squeeze(trajectorys(ii, :, :)), K, T, radarT(jj), parameter, RadarPos(jj));
    end
end

save trajectorys.mat trajectorys -mat;
save meas.mat meas -mat;

radarT = [T, T, T];
plotOneTraj(squeeze(trajectorys(1, :, :)), squeeze(meas(1, :, :, :)), RadarPos, radarT, T, K);
end

