import scipy.io as scio
import numpy as np
from torch.utils.data import Dataset, DataLoader
import copy


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


def centerMax(meas_, traj_, Dmax=1e4, Vmax=10):  # center-max归一化方式
    meas1 = copy.deepcopy(meas_)  # 作恢复使用
    meas = copy.deepcopy(meas_)
    traj = copy.deepcopy(traj_)
    for i in range(meas.shape[0]):
        for j in range(meas.shape[1]):
            meas[i, j, 1, :] = (meas[i, j, 1, :] - meas[i, j, 1, 0]) / Dmax
            meas[i, j, 0, :] = (meas[i, j, 0, :] - meas[i, j, 0, 0]) / Dmax
            cx = [meas[i, j, 0, 0], meas[i, j, 1, 0]]
        traj[i, 0, :] = (traj[i, 0, :] - cx[0])
        traj[i, 1, :] = (traj[i, 1, :] - cx[1])
        traj[i] = np.divide(traj[i].T, np.array([Dmax, Vmax, 1, Dmax, Vmax, 1])).T
    return meas, traj, meas1


def antiCenterMax(meas_, traj_, meas1, Dmax=1e4, Vmax=10):  # 反center-max 还原数据
    meas = copy.deepcopy(meas_)
    traj = copy.deepcopy(traj_)
    for i in range(meas.shape[0]):
        for j in range(meas.shape[1]):
            meas[i, j, 1, :] = (meas[i, j, 1, :] + meas1[i, j, 1, 0]) * Dmax
            meas[i, j, 0, :] = (meas[i, j, 0, :] + meas1[i, j, 0, 0]) * Dmax
            cx = [meas1[i, j, 0, 0], meas1[i, j, 1, 0]]
        traj[i] = np.dot(traj[i].T, np.array([Dmax, Vmax, 1, Dmax, Vmax, 1])).T
        traj[i, 0, :] = (traj[i, 0, :] + cx[0])
        traj[i, 1, :] = (traj[i, 1, :] + cx[1])
    return meas, traj


def createDatasets(meas, traj, Dmax=1e4, Vmax=10, fun="center-max"):  # 生成dataloader，并进行归一化操作
    if fun == "center-max":
        meas, traj, meas1 = centerMax(meas, traj, Dmax, Vmax)
        return trajDatasets(meas, traj, meas1)


class trajDatasets(Dataset):
    def __init__(self, meas, traj, meas1):
        self.meas = meas
        self.traj = traj
        self.meas1 = meas1


    def __len__(self):
        return self.meas.shape[0]

    def __getitem__(self, item):
        return self.meas[item], self.traj[item], self.meas1[item]


if __name__ == "__main__":
    trajectorys, meas = readData()

    #trainMeas, trainTraj, testMeas, testTraj = divideData(trajectorys, meas)

    #trainDatasets = createDatasets(trainMeas, trainTraj)

    meas__, traj__, meas1 = centerMax(meas, trajectorys)
    meas_, traj_ = antiCenterMax(meas__, traj__, meas1)

    print(meas_.all() == meas__.all())
    print(traj_.all() == trajectorys.all())
