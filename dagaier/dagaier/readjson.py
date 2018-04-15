# -*- coding: utf-8 -*-
import json
import cx_Oracle
import uuid
from DBUtils.PooledDB import PooledDB

pool = PooledDB(cx_Oracle, user = "wkai", password = "wkai", dsn = "127.0.0.1:1521/wkai",mincached=2,maxcached=33,maxshared=33,maxconnections=2)

def createPowerShellScript(type):
    '''
    生成下载脚本
    :param type: 1 linux  2 powershell
    :return:
    '''
    local = 'd:\\fileloc\\dagaier\\'
    f = open("D:\\Workspaces_python\\scrapy\\dagaier\\dagaier.json")
    fo = open("dagaier.sh", "w")
    if type == 2:

        fo.write( '$client = new-object System.Net.WebClient')
        entitys = json.load(f)
        for a in entitys:
            path = local+a['id']
            # print 'mkdir %s' % (path)
            fo.write( 'mkdir %s\n' % (path))
            for b in a['pictures']:
                print "$client.DownloadFile('%s', '%s')" % (b,path+'\\'+b.split('/')[-1])
                fo.write("$client.DownloadFile('%s', '%s')\n" % (b,path+'\\'+b.split('/')[-1]))
    else :
        '''
        mkdir XXXX
        cd XXXXX
        wget
        cd ..
        '''
        entitys = json.load(f)
        for a in entitys:
            fo.write( 'mkdir %s\ncd %s\n' % (a['id'],a['id']))
            for b in a['pictures']:
                fo.write("wget --no-check-certificate %s\n" % (b))
            fo.write( 'cd ..\n')
    fo.close()

def saveDagaierPicInfoToDB():
    '''
    从爬虫生成的json文件读取信息
    将page-pic 信息保存到数据库
    :return:
    '''
    con = pool.connection()
    cursor = con.cursor()

    f = open("D:\\Workspaces_python\\scrapy\\dagaier\\dagaier.json")
    entitys = json.load(f)
    for a in entitys:
        try:
            url  = a['url']
            tmp = a['url'].split('/')
            id = tmp[-2]+tmp[-1]
            name = a['name']
            num = len(a['pictures'])

            cursor.execute("insert into DAGAIERPAGE (ID, URL, NAME, NUM) values ('%s', '%s', '%s', %d)" % (id, url, name, num))
            con.commit()

            for b in a['pictures']:
                try:
                    picid = b.split('/')[-1]
                    cursor.execute("insert into DAGAIERPIC (UUID, PAGEID, PICID, URL, FLAG) values ('%s', '%s', '%s', '%s', '%s')" % (uuid.uuid1().hex, id, picid, b, '0'))
                    con.commit()
                except Exception as e:
                    print e
                    print 'dagaier picture %s error' % (b)
                    break
        except Exception as e:
            print e
            print 'dagaier page %s error' % (url)

    f.close()
    con.close()

if __name__=='__main__':
    createPowerShellScript(1)
