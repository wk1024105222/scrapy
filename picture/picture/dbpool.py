# encoding: utf-8
import cx_Oracle
from DBUtils.PooledDB import PooledDB
import redis
import pymysql;
import dbconfig as Config;

# pool = PooledDB(cx_Oracle, user = "wkai", password = "wkai", dsn = "127.0.0.1:1521/wkai",mincached=2,maxcached=33,maxshared=33,maxconnections=2)

pool = PooledDB(creator=pymysql, mincached=Config.DB_MIN_CACHED , maxcached=Config.DB_MAX_CACHED,
                                   maxshared=Config.DB_MAX_SHARED, maxconnections=Config.DB_MAX_CONNECYIONS,
                                   blocking=Config.DB_BLOCKING, maxusage=Config.DB_MAX_USAGE,
                                   setsession=Config.DB_SET_SESSION,
                                   host=Config.MYSQL_WKAI_HOST , port=Config.MYSQL_WKAI_PORT ,
                                   user=Config.MYSQL_WKAI_USER , passwd=Config.MYSQL_WKAI_PASSWORD ,
                                   db=Config.MYSQL_WKAI_DBNAME , use_unicode=False, charset=Config.DB_CHARSET);