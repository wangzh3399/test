import logging
import pymysql
import configparser
import traceback
import datetime
import re
from django.db import connection
from wechatpy import messages
from wechatpy.client.api import customservice

logger = logging.getLogger()
fh = logging.FileHandler('./logs/djangoserver.log', encoding='utf-8', mode='a')
formatter = logging.Formatter("%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)

def table_exists(table_name):
    return table_name in connection.introspection.table_names()

def getDBConn():
    globalconfig = configparser.ConfigParser()
    globalconfig.read('./globalconfig.ini', encoding='utf-8')
    globalconfig.sections() 
    if globalconfig.get('env', 'env') == 'prd':
        #生产环境
        host = globalconfig.get('prd', 'host')
        user = globalconfig.get('prd', 'user')
        passwd = globalconfig.get('prd', 'passwd')
        database = globalconfig.get('prd', 'database')
    else:
        #开发环境
        host = globalconfig.get('dev', 'host')
        user = globalconfig.get('dev', 'user')
        passwd = globalconfig.get('dev', 'passwd')
        database = globalconfig.get('dev', 'database')
    try:
        db = pymysql.connect(host=host,
                            user=user,
                            password=passwd,
                            database=database)
    except:
        logger.error('get db cursor fail')
        logger.error(traceback.format_exc())
        return None
    return db
def stockcodeAddPrefix(stockcode):
    if stockcode.startswith('00') or stockcode.startswith('30'):
        return 'sz'+stockcode
    if stockcode.startswith('60') or stockcode.startswith('68'):
        return 'sh'+stockcode
    if stockcode.startswith('sh') or stockcode.startswith('sz'):
        return stockcode
    assert 0
def stockcodeDelPrefix(stockcode):
    return re.findall('\d\d\d\d\d\d')[0]
def readCfg(section,key):
    globalconfig = configparser.ConfigParser()
    globalconfig.read('./globalconfig.ini', encoding='utf-8')
    sectionList = globalconfig.sections()
    if section not in sectionList:
        logger.error('section:'+section+' not in globalconfig')
        return False
    return globalconfig.get(section,key)
def writeCfg(section,key,value):
    globalconfig = configparser.ConfigParser()
    globalconfig.read('./globalconfig.ini', encoding='utf-8')
    globalconfig.set(section,key,value)  #修改db_port的值为69
    globalconfig.write(open('./globalconfig.ini', 'w'))
    return True
def getLastTradeDate():
    #获取最后一个交易日
    t = datetime.datetime.now()
    timestamp = t.timestamp()
    weekday = t.isoweekday()
    if weekday == 7:
        return datetime.datetime.fromtimestamp (timestamp - (86400 * 2)).strftime("%Y-%m-%d")
    elif weekday == 6:
        return datetime.datetime.fromtimestamp (timestamp - 86400).strftime("%Y-%m-%d")
    else:
        return t.strftime("%Y-%m-%d")
def getLastWeekLastTradeDate(curDate):
    #获取上一周周五
    dt = datetime.datetime.strptime(curDate, '%Y-%m-%d')
    weekday = dt.isoweekday()
    timestamp = dt.timestamp()
    return datetime.datetime.fromtimestamp (timestamp - (86400 * (weekday+2))).strftime("%Y-%m-%d")
def getLastMonthLastTradeDate(curDate):
    dt = datetime.datetime.strptime(curDate, '%Y-%m-%d')
    monday = curDate.isoweekday()
if __name__ == '__main__':
    print('do nothing')
    print(getLastTradeDate())