# -*- coding: utf-8 -*-
from picture.dbpool import pool


if __name__=='__main__':

    con = pool.connection()
    cursor = con.cursor()
    # 取20160701前上市的股票 从20170101 开始统计 避开上市初期的涨幅
    cursor.execute("select code from STOCKINFO where LISTEDDATE <= '2016-07-01'")
    for tmp in cursor.fetchall():
        code = tmp[0]
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
              "order by  d.date" % (code,'2017-01-01',code,'2017-01-01','2017-01-01','2018-09-27')
        cursor.execute(sql)
        dayDatas = list(cursor.fetchall())
        if dayDatas == None:
            continue
        length = len(dayDatas)
        dayresult = []

        for i in range(0,length,1):
            #代码 日期 open 送股 派息 转入金额 派息总额 当日购买数 送股数  股票总数 余额 成本
            if i==0 :
                ytdbalance = 0
                ytdStockTotal = 0
                ytdCost=0
            else :
                ytdbalance = dayresult[i-1][10]
                ytdStockTotal = dayresult[i-1][9]
                ytdCost = dayresult[i-1][11]

            txndate = dayDatas[i][1]
            open = float(dayDatas[i][2])
            giveStockRate = int(dayDatas[i][3])
            giveMoneyRate = float(dayDatas[i][4])

            if txndate.endswith('01'):
                #卡转证券
                tranAmount = 1000
                tranFlag = '0'
            else:
                tranAmount = 0

            giveMoney=ytdStockTotal/10*giveMoneyRate
            giveStock = ytdStockTotal / 10 * giveStockRate

            if tranFlag=='0' and open>0:
                buyStock = (tranAmount+giveMoney+ytdbalance)//(open*100)*100
                tranFlag='1'
            else  :
                buyStock=0

            stockTotal = ytdStockTotal+buyStock+giveStock
            balance = ytdbalance+tranAmount+giveMoney-(buyStock*open)
            cost = ytdCost+tranAmount

            dayresult.append((code,txndate,open,giveStockRate,giveMoneyRate,tranAmount,giveMoney,buyStock,giveStock,stockTotal,round(balance,2),cost))
    con.close()



