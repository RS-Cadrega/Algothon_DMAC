import pandas as pd
import numpy as np
import time

ALL_DATA = []

best_tuples = []

dlrPosLimit = 10000

commRate = 0.0025


def loadPrices(fn):
    global nt, nInst
    df = pd.read_csv(fn, sep='\s+', header=None, index_col=None)
    nt, nInst = df.values.shape
    return (df.values).T


pricesFile = "./prices.txt"
ALL_DATA = loadPrices(pricesFile)

last = time.time()

with open('/Users/kevinzhou/PycharmProjects/Algothon2022_(DMAC)/best_tuple_info', 'r') as f:
    for line in f.readlines():
        red1 = line.strip('\n')
        red2 = red1.strip('(')
        red3 = red2.strip(')')
        #print(tuple(map(int, red3.split(', '))))
        best_tuples.append(tuple(map(int, red3.split(', '))))

def log(s):
    global last
    spend = int((time.time() - last) * 1000)
    last = time.time()
    print(f"{spend}: {s}")


def train(data, stock, l, s):
    (plmu, ret, annSharpe, totDVolume) = (0,0,0,0)

    cur_position = np.zeros(nInst)
    cash = 0
    totDVolume = 0
    value = 0
    todayPLL = []
    (_, nt) = data.shape
    for day in range(200):
        old_pos = cur_position.copy()
        if day < l + 1:
            continue
        p_long_ave = sum(data[stock][day - l - 1:day - 1]) / l
        p_short_ave = sum(data[stock][day - s - 1:day - 1]) / s
        long_ave = sum(data[stock][day - l:day]) / l
        short_ave = sum(data[stock][day - s:day]) / s
        if long_ave >= short_ave and p_long_ave < p_short_ave:
            cur_position[stock] = -100
        if long_ave <= short_ave and p_long_ave > p_short_ave:
            cur_position[stock] = 100
        newPosOrig = cur_position.copy()
        curPrices = data[:, day]  # prcHist[:,t-1]
        deltaPos = newPosOrig - old_pos
        dvolumes = curPrices * np.abs(deltaPos)
        dvolume = np.sum(dvolumes)
        totDVolume += dvolume
        comm = dvolume * commRate
        cash -= curPrices.dot(deltaPos) + comm
        old_pos = np.array(newPosOrig)
        posValue = old_pos.dot(curPrices)
        todayPL = cash + posValue - value
        todayPLL.append(todayPL)
        value = cash + posValue
        ret = 0.0
        if (totDVolume > 0):
            ret = value / totDVolume
    pll = np.array(todayPLL)
    (plmu, plstd) = (np.mean(pll), np.std(pll))
    annSharpe = 0.0
    if (plstd > 0):
        annSharpe = 16 * plmu / plstd
    return (plmu, ret, annSharpe, totDVolume)


def getBest(data: object, stock: object) -> object:
    best_return = 0
    best_sharpe = 0
    opt = (0, 0)
    for i in range(20, 80):
        for j in range(10, i - 10):
            (plmu, ret, annSharpe, totDVolume) = train(data, stock, i, j)
            if best_return < ret:
                best_return = ret
                opt = (i, j)
            if best_sharpe < annSharpe:
                best_sharpe = annSharpe
                # print(profit, required, i, j)
    if best_sharpe < 1.2 or best_return < 0.05:
        return (0, 0)
    return ((opt))

# with open('/Users/kevinzhou/PycharmProjects/Algothon2022_(DMAC)/best_tuple_info', 'w') as f:
#     for i in range(100):
#         log(f"Training stock: {i}")
#         f.write(str(getBest(ALL_DATA[:200], i)) + '\n')

#print("Finished best_tuples")

def getMyPosition(data):
    cur_position = [0] * 100
    for day in range(len(data[0])):
        for stock in range(len(data)):
            l = best_tuples[stock][0]
            s = best_tuples[stock][1]
            if l == 0:
                continue
            if day < l + 1:
                continue
            p_long_ave = sum(data[stock][day - l - 1:day - 1]) / l
            p_short_ave = sum(data[stock][day - s - 1:day - 1]) / s
            long_ave = sum(data[stock][day - l:day]) / l
            short_ave = sum(data[stock][day - s:day]) / s
            if long_ave >= short_ave and p_long_ave < p_short_ave:
                cur_position[stock] = -100
            if long_ave <= short_ave and p_long_ave > p_short_ave:
                cur_position[stock] = 100
    return cur_position
