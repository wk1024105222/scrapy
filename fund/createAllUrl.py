#从全量页面中获取所有基金编号 生成所有url入库
import re
import urllib

from fund.dbpool import pool

dataType=['jbgk', 'jjjl', 'jjjz', 'fhsp', 'zcpz', 'gmbd']
url = 'http://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx?t=1&lx=1&letter=&gsid=&text=&sort=zdf,desc&page=1,9999&feature=|&dt=1552447261268&atfc=&onlySale=0'
pageHtml = urllib.urlopen(url).read()
reg = re.compile(r'"(\d{6})"')
rlt = re.findall(reg, pageHtml)

con = pool.connection()
cursor = con.cursor()
for code in rlt:
    # urls=['http://fundf10.eastmoney.com/'+type+'_'+code+'.html' for type in dataType ]
    # # for url in urls:
    for type in dataType:
        url = 'http://fundf10.eastmoney.com/%s_%s.html' % (type,code)
        cursor.execute("INSERT INTO fund_dataurl VALUES ('%s','%s','%s', '%s');" % (code,type,url, '0'))
        con.commit()
        # yield Request(url, callback=self.parse_item, dont_filter=True)
con.close()