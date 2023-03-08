import scipy.io as scio
import numpy as np
from torch.utils.data import Dataset, DataLoader


def readData():  # 读取数据
    trajectorys = scio.loadmat('./matlabFun/trajectorys.mat')['trajectorys']
    trajectorys = np.array(trajectorys).astype('float32')
    print("trajectorys.size=", trajectorys.shape)

    meas = scio.loadmat('./matlabFun/meas.mat')['meas']
    meas = np.array(meas).astype('float32')
    print("meas.size=", meas.shape)

    return trajectorys, meas


def divideData(trajectorys, meas, divideDataRatio=0.8):  # 划分数据集
    dataLen = trajectorys.shape[0]

    trainDataLen = int(divideDataRatio * dataLen)
    trainMeas = meas[0:trainDataLen, :, :, :]  # datasize * radarNums * dimZ * K
    trainTraj = trajectorys[0:trainDataLen, :, :]  # datasize * dimX * K

    testMeas = meas[trainDataLen:, :, :, :]  # datasize * radarNums * dimZ * K
    testTraj = trajectorys[trainDataLen:, :, :]  # datasize * dimX * K

    print("trainData size=", trainDataLen)
    print("testData size=", dataLen - trainDataLen)

    return trainMeas, trainTraj, testMeas, testTraj


def centerMax(meas, traj, Dmax=1e4, Vmax=10):  # center-max归一化方式
    for i in range(meas.shape[0]):
        for j in range(meas.shape[1]):
            meas[i, j, 1, :] = (meas[i, j, 1, :] - meas[i, j, 1, 0]) / Dmax
            meas[i, j, 0, :] = (meas[i, j, 0, :] - meas[i, j, 0, 0]) / Dmax
            cx = [meas[i, j, 0, 0], meas[i, j, 1, 0]]
        traj[i, 0, :] = (traj[i, 0, :] - cx[0])
        traj[i, 1, :] = (traj[i, 1, :] - cx[1])
        traj[i] = np.divide(traj[i].T, np.array([Dmax, Vmax, 1, Dmax, Vmax, 1])).T
    return meas, traj


def createDatasets(meas, traj, Dmax=1e4, Vmax=10, fun="center-max"):  # 生成dataloader，并进行归一化操作
    if fun == "center-max":
        meas, traj = centerMax(meas, traj, Dmax, Vmax)
        return trajDatasets(meas, traj)


class trajDatasets(Dataset):
    def __init__(self, meas, traj):
        self.meas = meas
        self.traj = traj

    def __len__(self):
        return self.meas.shape[0]

    def __getitem__(self, item):
        return self.meas[item], self.traj[item]


if __name__ == "__main__":
    trajectorys, meas = readData()

    trainMeas, trainTraj, testMeas, testTraj = divideData(trajectorys, meas)

    trainDatasets = createDatasets(trainMeas, trainTraj)
