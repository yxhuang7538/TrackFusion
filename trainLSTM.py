import torch
import argparse

from processData import *
from models import LSTM

if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

if __name__ == "__main__":
    # -------------------- 参数设置 -------------------- #
    parser = argparse.ArgumentParser()
    parser.add_argument('--batchSize', type=int, default=32)
    parser.add_argument('--inputSize', type=int, default=6)
    parser.add_argument('--hiddenSize', type=int, default=64)
    parser.add_argument('--outputSize', type=int, default=6)
    parser.add_argument('--numLayers', type=int, default=2)
    parser.add_argument('--midLinearSize', type=int, default=32)
    parser.add_argument('--prevLoss', type=int, default=1000)
    parser.add_argument('--finalLoss', type=float, default=1e-4)
    parser.add_argument('--maxEpochs', type=int, default=2000)
    parser.add_argument('--printEpoch', type=int, default=1)
    parser.add_argument('--lr', type=float, default=1e-3)
    args = parser.parse_args()
    # ------------------------------------------------- #

    # -------------------- 读取数据 -------------------- #
    trajectorys, meas = readData()
    trainMeas, trainTraj, testMeas, testTraj = divideData(trajectorys, meas)

    trainDatasets = createDatasets(trainMeas, trainTraj)
    trainSet = DataLoader(trainDatasets, batch_size=args.batchSize, shuffle=True)

    testDatasets = createDatasets(testMeas, testTraj)
    testSet = DataLoader(testDatasets, batch_size=1, shuffle=True)
    # ------------------------------------------------- #

    # -------------------- 构建网络 -------------------- #
    model = LSTM.model(args.inputSize, args.hiddenSize, args.outputSize,
                           args.midLinearSize, args.numLayers)
    if device == torch.device("cuda"):
        model = model.cuda()
    print('LSTM model:', model)
    print('model.parameters:', model.parameters)

    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)
    # ------------------------------------------------- #

    # -------------------- 训练网络 -------------------- #
    for epoch in range(args.maxEpochs):
        for meas, traj, _ in trainSet:
            model.zero_grad()
            measTensor = meas.to(device)
            trajTensor = traj.to(device)
            output = model(measTensor)
            loss = criterion(output, trajTensor)
            loss.backward()
            optimizer.step()

        if loss < args.prevLoss:
            torch.save(model.state_dict(), 'lstmModel.pt')  # save model parameters to files
            prev_loss = loss

        if loss.item() < args.finalLoss:
            print('Epoch [{}/{}], Loss: {:.5f}'.format(epoch + 1, args.maxEpochs, loss.item()))
            print("The loss value is reached")
            break
        elif (epoch + 1) % args.printEpoch == 0:
            print('Epoch: [{}/{}], Loss:{:.5f}'.format(epoch + 1, args.maxEpochs, loss.item()))

    # ------------------------------------------------- #


