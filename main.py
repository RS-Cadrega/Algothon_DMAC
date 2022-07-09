import pandas as pd

data = []

best_tuples = []

with open("/Users/kevinzhou/Downloads/Algothon/algothon2022-starter-code/prices.txt") as f:
    for line in f.readlines():
        words = line.split(' ')
        nums = []
        for word in words:
            word = word.strip()
            if word == '':
                continue
            nums.append(float(word))
        data.append(nums)


data_cut = data[150:]

def getProfit(data):
    cur_position = [0]*100
    profit = 0
    stock_data = list((zip(*list(reversed(data[::-1])))))
    required = 1
    liquidity = 0
    for day in range(len(data)):
        print(day)
        for stock in range(len(stock_data)):
            l = best_tuples[stock][0]
            s = best_tuples[stock][1]
            if l==0:
                continue
            if day < l + 1:
                continue
            p_long_ave = sum(stock_data[stock][day-l-1:day-1])/l
            p_short_ave = sum(stock_data[stock][day-s-1:day-1])/s
            long_ave = sum(stock_data[stock][day - l:day])/l
            short_ave = sum(stock_data[stock][day - s:day])/s
            if long_ave >= short_ave and p_long_ave < p_short_ave:
                diff = 2 + cur_position[stock]
                cur_position[stock] = -2
                profit += diff*data[day][stock]
                liquidity += diff*data[day][stock]
            if long_ave <= short_ave and p_long_ave > p_short_ave:
                diff = 2 - cur_position[stock]
                cur_position[stock] = 2
                profit -= diff*data[day][stock]
                liquidity -= diff*data[day][stock]
            if liquidity < 0:
                required -= liquidity
                liquidity = 0

    for stock in range(100):
        if cur_position[stock] == -2:
            profit -= 2*data[len(data) - 1][stock]
            cur_position[stock] += 2
            liquidity += 2*data[len(data) - 1][stock]
        if cur_position[stock] == 2:
            profit += cur_position[stock]*data[len(data) - 1][stock]
            cur_position[stock] -= 2
            liquidity -= 2 * data[len(data) - 1][stock]
    return profit, required

def getProfit2(data, stock_data, l, s):
    cur_position = [0]*100
    profit = 0
    required = 1
    liquidity = 0
    for day in range(200):
        if day < l+1:
            continue
        for stock in range(len(stock_data)):
            p_long_ave = sum(stock_data[stock][day-l-1:day-1])/l
            p_short_ave = sum(stock_data[stock][day-s-1:day-1])/s
            long_ave = sum(stock_data[stock][day - l:day])/l
            short_ave = sum(stock_data[stock][day - s:day])/s
            if long_ave >= short_ave and p_long_ave < p_short_ave:
                diff = 2 + cur_position[stock]
                cur_position[stock] = -2
                profit += diff*data[day][stock]
                liquidity += diff*data[day][stock]
            if long_ave <= short_ave and p_long_ave > p_short_ave:
                diff = 2 - cur_position[stock]
                cur_position[stock] = 2
                profit -= diff*data[day][stock]
                liquidity -= diff*data[day][stock]
            if liquidity < 0:
                required -= liquidity
                liquidity = 0

    for stock in range(100):
        if cur_position[stock] == -2:
            profit -= 2*data[199][stock]
            cur_position[stock] += 2
            liquidity += 2*data[199][stock]
        if cur_position[stock] == 2:
            profit += cur_position[stock]*data[199][stock]
            cur_position[stock] -= 2
            liquidity -= 2 * data[199][stock]
    return profit, required

def getBest(data, stock_data):
    cur_best = 0
    best_return = 0
    opt = (0, 0)
    for i in range(20, 80):
        for j in range(10, i - 10):
            info = getProfit2(data,stock_data, i, j)
            profit = info[0]
            required = info[1]
            if best_return < profit/required:
                best_return = profit/required
                opt = (i, j)
                #print(profit, required, i, j)
    return((opt))

for i in range(100):
    stock_data = list((zip(*list(reversed(data[::-1])))))[i:i+1]
    best_tuples.append(getBest(data, stock_data))



#print(getProfit(data_cut))























def getProfit(data, l, s):
    cur_position = [0]*100
    profit = 0
    stock_data = list((zip(*list(reversed(data[::-1])))))[1:2]
    required = 1
    liquidity = 0
    for day in range(200):
        if day < l+1:
            continue
        for stock in range(len(stock_data)):
            p_long_ave = sum(stock_data[stock][day-l-1:day-1])/l
            p_short_ave = sum(stock_data[stock][day-s-1:day-1])/s
            long_ave = sum(stock_data[stock][day - l:day])/l
            short_ave = sum(stock_data[stock][day - s:day])/s
            if long_ave >= short_ave and p_long_ave < p_short_ave:
                diff = 2 + cur_position[stock]
                cur_position[stock] = -2
                profit += diff*data[day][stock]
                liquidity += diff*data[day][stock]
            if long_ave <= short_ave and p_long_ave > p_short_ave:
                diff = 2 - cur_position[stock]
                cur_position[stock] = 2
                profit -= diff*data[day][stock]
                liquidity -= diff*data[day][stock]
            if liquidity < 0:
                required -= liquidity
                liquidity = 0

    for stock in range(100):
        if cur_position[stock] == -2:
            profit -= 2*data[199][stock]
            cur_position[stock] += 2
            liquidity += 2*data[199][stock]
        if cur_position[stock] == 2:
            profit += cur_position[stock]*data[199][stock]
            cur_position[stock] -= 2
            liquidity -= 2 * data[199][stock]
    return profit, required

def getProfitold(data, stock_data, l, s):
    cur_position = [0]*100
    profit = 0
    required = 1
    liquidity = 0
    for day in range(200):
        if day < l+1:
            continue
        for stock in range(len(stock_data)):
            p_long_ave = sum(stock_data[stock][day-l-1:day-1])/l
            p_short_ave = sum(stock_data[stock][day-s-1:day-1])/s
            long_ave = sum(stock_data[stock][day - l:day])/l
            short_ave = sum(stock_data[stock][day - s:day])/s
            if long_ave >= short_ave and p_long_ave < p_short_ave:
                diff = 2 + cur_position[stock]
                cur_position[stock] = -2
                profit += diff*data[day][stock]
                liquidity += diff*data[day][stock]
            if long_ave <= short_ave and p_long_ave > p_short_ave:
                diff = 2 - cur_position[stock]
                cur_position[stock] = 2
                profit -= diff*data[day][stock]
                liquidity -= diff*data[day][stock]
            if liquidity < 0:
                required -= liquidity
                liquidity = 0

    for stock in range(100):
        if cur_position[stock] == -2:
            profit -= 2*data[199][stock]
            cur_position[stock] += 2
            liquidity += 2*data[199][stock]
        if cur_position[stock] == 2:
            profit += cur_position[stock]*data[199][stock]
            cur_position[stock] -= 2
            liquidity -= 2 * data[199][stock]
    return profit, required

