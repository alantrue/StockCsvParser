# -*- coding: utf-8 -*-

import csv
import re
import string
import os

os.chdir("E:\\StockData")
files = os.listdir("E:\\StockData")

#指數(0) 收盤指數(1) 漲跌(2)(+/-) 漲跌點數(3) 漲跌百分比(4)(%)
#加權股價指數
tseaName = u'加權股價指數'.encode("utf-8")


#證券代號(0) 證券名稱(1) 成交股數(2) 成交筆數(3) 成交金額(4) 開盤價(5) 最高價(6) 最低價(7) 收盤價(8) 漲跌(9)(+/-) 漲跌價差(10) 最後揭示買價(11) 最後揭示買量(12) 最後揭示賣價(13) 最後揭示賣量(14) 本益比(15)

def getTsea(file):
    with open(file, 'r') as f:
        reader = csv.reader(f)
        i = 0
        for row in reader:
            i += 1
            if i != 3:
                continue

            price = float(row[1].replace(',', ''))
            changeRate = float(row[4]) / 100
            return [price, changeRate]

def getTesaRate(file1, file2):
    tsea1 = getTsea(file1)
    tsea2 = getTsea(file2)

    changeRate1 = (tsea1[0] - tsea2[0]) / tsea2[0]
    changeRate2 = tsea1[1]

    return [changeRate1, changeRate2]


def getStockMap(file):
    stockMap = dict()
    with open(file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 16:
                id = row[0]
                price = row[8]
                try:
                    float(price)
                    if id[0] != '0' and id.isdigit():
                        stockMap[id] = row
                except:
                    pass

    return stockMap

def getStockList(file):
    stockList = []
    with open(file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 16:
                id = row[0]
                price = row[8]
                try:
                    float(price)
                    if id[0] != '0' and id.isdigit():
                        stockList.append(row)
                except:
                    pass

    return stockList

def CalTotalRate(stocks, yesterdayStocks):
    value1 = 0
    total1 = 0

    value2 = 0
    total2 = 0

    for s in stocks:
        id = s[0]
        try:
            ys = yesterdayStocks[id]
            yclose = float(ys[8])
            close = float(s[8])
            changeRate = (close - yclose) / yclose
            tradeValue = float(s[4].replace(',', ''))
            value1 += changeRate * tradeValue
            total1 += tradeValue
        except:
            pass

        try:
            open = float(s[5])
            close = float(s[8])
            changeRate = (close - open) / open
            tradeValue = float(s[4].replace(',', ''))
            value2 += changeRate * tradeValue
            total2 += tradeValue
        except:
            pass

    return [(value1 / total1), (value2 / total2)]

def getRate(file1, file2):
    stocks = getStockList(file1)

    if len(stocks) == 0:
        return

    stocks = sorted(stocks, key=lambda stock: float(stock[8]), reverse=True)

    big = stocks[0:len(stocks)//3]
    medium = stocks[len(stocks)//3: len(stocks)*2//3]
    small = stocks[len(stocks)*2//3: len(stocks)]

    yesterdayStocks = getStockMap(file2)

    bigRate = CalTotalRate(big, yesterdayStocks)
    mediumRate = CalTotalRate(medium, yesterdayStocks)
    smallRate = CalTotalRate(small, yesterdayStocks)

    day = file1.split('.')[0]
    d = "{0}/{1}/{2}".format(day[0:4], day[4:6], day[6:8])
    b1 = "{0:.5f}".format(bigRate[0])
    m1 = "{0:.5f}".format(mediumRate[0])
    s1 = "{0:.5f}".format(smallRate[0])
    b2 = "{0:.5f}".format(bigRate[1])
    m2 = "{0:.5f}".format(mediumRate[1])
    s2 = "{0:.5f}".format(smallRate[1])

    tsea = getTesaRate(files[i+1], files[i])

    return [d, b1, m1, s1, tsea[0], b2, m2, s2, tsea[1]]

datas = []

for i in range(len(files)-1):
    data = getRate(files[i+1], files[i])
    datas.append(data)

with open('E:\\result1.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerow(["date", "high", "medium", "low", "tsea"])
    for data in datas:
        writer.writerow(data[0:5])

with open('E:\\result2.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerow(["date", "high", "medium", "low", "tsea"])
    for data in datas:
        writer.writerow([data[0], data[5], data[6], data[7], data[8]])

print("done")