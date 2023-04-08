import logging
import pymysql
import configparser
import traceback
import datetime


logger = logging.getLogger()
fh = logging.FileHandler('./logs/djangoserver.log', encoding='utf-8', mode='a')
formatter = logging.Formatter("%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)



def getDBConn():
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
    return db

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
if __name__ == '__main__':
    print('do nothing')