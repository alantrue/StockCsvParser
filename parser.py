import csv
import re
import string

def printRate(file):
    stocks = []
    with open(file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 16:
                id = row[0]
                price = row[8]
                try:
                    float(price)
                    if id[0] != '0' and id.isdigit():
                        stocks.append(row)
                except:
                    pass

    if len(stocks) == 0:
        return

    """證券代號,證券名稱,成交股數,成交筆數,成交金額,開盤價,最高價,最低價,收盤價,漲跌(+/-),漲跌價差,最後揭示買價,最後揭示買量,最後揭示賣價,最後揭示賣量,本益比"""
    stocks = sorted(stocks, key=lambda stock: float(stock[8]), reverse=True)


    big = stocks[0:len(stocks)//3]
    medium = stocks[len(stocks)//3: len(stocks)*2//3]
    small = stocks[len(stocks)*2//3: len(stocks)]

    bigRate = CalTotalRate(big)
    mediumRate = CalTotalRate(medium)
    smallRate = CalTotalRate(small)

    print(file)
    print("高:", bigRate)
    print("中:", mediumRate)
    print("低:", smallRate)
    if smallRate < 0:
        print("漲")
    else:
        print("跌")
    print("")

def CalTotalRate(stocks):
    value = 0
    total = 0

    for s in stocks:
        open = float(s[5])
        close = float(s[8])
        changeRate = (close - open) / open
        tradeValue = float(s[4].replace(',', ''))
        value += changeRate * tradeValue
        total += tradeValue

    return (value / total)

printRate('Data\\20130101.csv');
printRate('Data\\20130102.csv');


