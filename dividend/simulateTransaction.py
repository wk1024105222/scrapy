# -*- coding: utf-8 -*-
from picture.dbpool import pool

if __name__=='__main__':

    con = pool.connection()
    cursor = con.cursor()
    # 取20160701前上市的股票 从20170101 开始统计 避开上市初期的涨幅
    cursor.execute("select code from stockdata_163 group by code having min(txndate) <= '2016-07-01'")
    begindate = '2017-01-01'
    enddate = '2018-10-24'

    for tmp in cursor.fetchall():
        # code=tmp[0]
        code = '000860'
        sql = "select c.code,d.date txndate,ifnull(c.open,0),ifnull(c.givestock,0),ifnull(c.givemoney,0) from datelist d " \
              "left join " \
              "( select a.code,a.TXNDATE ,ifnull(a.OPEN,0) open,(ifnull(b.stockDividend,0)+ifnull(b.transfeShares,0)) givestock ,ifnull(b.dividendPayout,0) givemoney from stockdata_163 a " \
              "left join stockdevidend b on a.code=b.code and a.TXNDATE=b.date3  " \
              "where a.code='%s' and a.txndate >'%s'  " \
              "union  " \
              "select b.CODE,b.date3 txndate,ifnull(a.OPEN,0) open,(ifnull(b.stockDividend,0)+ifnull(b.transfeShares,0)) givestock,ifnull(b.dividendPayout,0) givemoney from stockdata_163 a " \
              "right join stockdevidend b on a.code=b.code and a.TXNDATE=b.date3  " \
              "where b.code='%s' and b.date3>='%s') c  " \
              "on d.date=c.txndate  " \
              "where d.date >='%s' and d.date <='%s'" \
              "order by  d.date" % (code, begindate, code, begindate, begindate, enddate)
        cursor.execute(sql)
        dayDatas = list(cursor.fetchall())
        if dayDatas == None:
            continue
        length = len(dayDatas)
        dayresult = []
        con.close()
        for i in range(0, length, 1):
            # 代码 日期 open 送股 派息 转入金额 派息总额 当日购买数 送股数  股票总数 余额 成本
            if i == 0:
                # 首月初始化0
                ytdbalance = 0
                ytdStockTotal = 0
                ytdCost = 0
            else:
                # 非首月 获取上期账户余额、持股总量、成本
                ytdbalance = dayresult[i - 1][10]
                ytdStockTotal = dayresult[i - 1][9]
                ytdCost = dayresult[i - 1][11]

            txndate = dayDatas[i][1]
            open = float(dayDatas[i][2])
            giveStockRate = int(dayDatas[i][3])
            giveMoneyRate = float(dayDatas[i][4])

            # 每月第一天
            if txndate.endswith('01'):
                # 卡转证券1000元
                tranAmount = 1000
                # 标记交易开始
                tranFlag = '0'
            else:
                tranAmount = 0

            # 派息金额
            giveMoney = ytdStockTotal / 10 * giveMoneyRate
            # 送股数
            giveStock = ytdStockTotal / 10 * giveStockRate

            # 若交易未完成 且当日开盘 则使用账户余额+转入金融+派息金额 使用开盘价买入，同时标记交易结束；否则交易未结束
            if tranFlag == '0' and open > 0:
                buyStock = (tranAmount + giveMoney + ytdbalance) // (open * 100) * 100
                tranFlag = '1'
            else:
                buyStock = 0

            # 持股总量=昨日持股数+送股数+今日成交数
            stockTotal = ytdStockTotal + buyStock + giveStock
            # 账户余额=昨日余额+转入金融+派息金额-交易金额
            balance = ytdbalance + tranAmount + giveMoney - (buyStock * open)
            # 成本=昨日成本+转入金融
            cost = ytdCost + tranAmount

            dayresult.append((code, txndate, open, giveStockRate, giveMoneyRate, tranAmount, giveMoney, buyStock, giveStock,stockTotal, round(balance, 2), cost))
            print (code, txndate, open, giveStockRate, giveMoneyRate, tranAmount, giveMoney, buyStock, giveStock,stockTotal,round(balance, 2), cost, round(stockTotal * open + balance - cost, 2))
        break




