# LSTM 网络融合

import torch.nn as nn

class model(nn.Module):
    def __init__(self, inputSize, hiddenSize, outputSize, midLinearSize, numLayers, bidirectional=False):
        super(model, self).__init__()
        # 输入是 序列长度 * （雷达个数 * 状态维度）
        # 输出是 序列长度 * 状态维度
        self.lstm = nn.LSTM(inputSize, hiddenSize, numLayers, bidirectional=bidirectional)
        self.linear1 = nn.Linear(hiddenSize, midLinearSize)
        self.linear2 = nn.Linear(midLinearSize, outputSize)

    def forward(self, _x):
        # 对_x的维度进行变换 _x : (batchsize, radarNums, dimZ, seqLen)
        batchsize, radarNums, dimZ, seqLen = _x.shape
        _x = _x.view(batchsize, radarNums * dimZ, seqLen)
        batchsize, dimZ, seqLen = _x.shape
        _x = _x.view(seqLen, batchsize, dimZ)

        x, _ = self.lstm(_x)  # _x是输入，(seq_len，batch，input_size)
        s, b, h = x.shape  # x是输出，(seq_len, batch, hidden_size)
        x = x.view(s * b, h)
        x = self.linear1(x)
        x = self.linear2(x)
        x = x.view(b, -1, s)
        return x

