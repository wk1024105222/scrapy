__author__ = 'wkai'
from gzlibrary.dbpool import pool

con = pool.connection()
cursor = con.cursor()

booktype = ['A','B','C','D','E','F','G','H','I','J','K','N','O','P','Q','R','S','T','U','V','X','Z']
booktypenum=[7274,80103,39826,112661,12162,176053,130216,79185,337841,99084,170755,9691,23076,14801,17423,92947,18334,212934,13387,2555,10295,37339]

for i in range(0,len(booktype),1) :
    pages = booktypenum[i]/1000+1
    for j in range(1,pages+1,1) :
        url = 'http://opac.gzlib.gov.cn/opac/search?q=%s&searchType=standard&isFacet=false' \
              '&view=simple&searchWay=class&booktype=1&rows=1000&sortWay=score&sortOrder=desc&libcode=GT&searchWay0=marc&logical0=AND&page=%s' % (booktype[i],j)
        sql = "insert into gzlibraryurl (booktype, pagenum,url,downflag )  values ('%s', '%d', '%s', '%s') " % (booktype[i],j,url,0)
        name = ''

        try:
            cursor.execute(sql)
            print (booktype[i],j,'save success')
        except Exception as e:
            print (booktype[i],j,'save failed')
    con.commit()
con.close()