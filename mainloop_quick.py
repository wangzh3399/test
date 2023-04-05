import multiprocessing as mp
import logging
import pymysql
import configparser
import traceback
from multiprocessing.managers import SharedMemoryManager
import datetime
import time
import akshare as ak
import decimal

logger = logging.getLogger()
fh = logging.FileHandler('./stockSpider.log', encoding='utf-8', mode='a')
formatter = logging.Formatter("%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.setLevel(logging.ERROR)



def getDBCursor():
    globalconfig = configparser.ConfigParser()
    globalconfig.read('./globalconfig.ini', encoding=None)
    globalconfig.sections() 
    if globalconfig.get('env', 'env') == 'prd':
        #生产环境
        host = globalconfig.get('prdmysqldb', 'host')
        user = globalconfig.get('prdmysqldb', 'user')
        passwd = globalconfig.get('prdmysqldb', 'passwd')
        database = globalconfig.get('prdmysqldb', 'database')
    else:
        #开发环境
        host = globalconfig.get('devmysqldb', 'host')
        user = globalconfig.get('devmysqldb', 'user')
        passwd = globalconfig.get('devmysqldb', 'passwd')
        database = globalconfig.get('devmysqldb', 'database')
    try:
        db = pymysql.connect(host=host,
                            user=user,
                            password=passwd,
                            database=database)
    except:
        logger.error('get db cursor fail')
        logger.error(traceback.format_exc())
        return None
    return db.cursor()
def checkData():
    logger.info('checkData')


def initEnv():
    #更新股票list，每个周六定时执行。
    logger.info('init envir')
    #启动时检查数据库完整性、表结构完整性
    if not checkDB():
        exit(0)
    logger.info('init envir successfully')
    return 0

def updateStockListPerDay():
    #每天凌晨更新股票列表，写文件到./stockList_rundata.txt
    logger.info('update stock list')

def buildShareMem():
    x = SharedMemoryManager().ShareableList(list(range(30),name = 'quickloop'))
    return x
def dataFormat(data,n):#取小数点后n位
    if n > 8:
        logger.error('not support len > 8,need modify the func')
        exit(0)
    data = str(data)
    logger.debug(data)
    #价格取小数点2位,NAN取值为0
    if data.lower() == 'nan':
        return str(0)
    if data.find('e') == 1:
        data = str(decimal.Decimal(data))
    try:
        if data.find('.') != -1:
            if len(data.split('.')[1]) < n :
                data = data+'00000000'
            logger.debug('deal with point,cut')
            return data.split('.')[0] + '.' + data.split('.')[1][:n]
    except :
        logger.error('data dealling with point occured error and exit')
        exit(0)
def getLastTradeDate():
    #获取最后一个交易日
    t = datetime.datetime.now()
    timestamp = t.timestamp()
    weekday = t.isoweekday()
    if weekday == 7:
        return datetime.datetime.utcfromtimestamp(timestamp - (86400 * 2))
    elif weekday == 6:
        return datetime.datetime.utcfromtimestamp(timestamp - 86400)
    else:
        return t

def quickloop():
    #采集股票基础信息,分时信息监控，先放内存里吧，不入库
    while True:
        logger.info('do quick loop'+str(mem))
        time.sleep(5)
if __name__ == '__main__':
    if not initEnv():
        exit(0)
    #mem = buildShareMem()
    #quick依赖slow的数据库表更新，可以一起拉起，但如果数据库表信息为空，则等待。
    quickloop()
    
    
    