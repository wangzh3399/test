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



def checkDBisErr():
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
    logger.info(f'Current environment is {globalconfig.get("env", "env")},do checkDB')
    try:
        db = pymysql.connect(host=host,
                            user=user,
                            password=passwd,
                            database=database)
    except:
        logger.error(f'Check DB failed,see the error:\r\n{traceback.format_exc()}')
        return None
    return db.cursor()
def buildStockStaticData(dbCursor):
    #不check表是否存在，默认环境已经生成表。这里默认先使用基础表添加股票信息，再由updateStockListPerDay来负责增量更新。
    stockFile = open('./stocklist.txt','r')
    for stock in stockFile:
        
def initEnv():
    #更新股票list，每个周六定时执行。
    logger.info('init envir')
    #启动时检查数据库完整性、表结构完整性，不完整则退出
    dbCursor = checkDBisErr()
    if dbCursor == None:
        exit(0)
    if buildStockStaticData(dbCursor) == None:
        exit(0)
    logger.info('init envir successfully')
    return 0

def updateStockListPerDay():
    #每天凌晨更新股票列表，写数据库。退市的保留，只增不删。 启动时判断，如果股票静态信息表如果为空则默认写一次，否则不写。

    logger.info('update stock list')

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

def updateSingleStockData(stockcode,dbCursor):
    #维护近三年的股票数据. stockcode 默认带sz sh等前缀
    t = datetime.datetime.now()
    month = '0' + str(t.month)
    day = '0' + str(t.day)
    startdate = str(t.year-3)+month[len(month)-2:]+day[len(day)-2:]
    enddate = str(t.year)+month[len(month)-2:]+day[len(day)-2:]
    lastTradeDate = getLastTradeDate()
    dealDuplicate = []
    dateInDBList = []
    try:
        cmd_select = 'select date from '+stockcode+';'
        dbCursor.execute(cmd_select)
        selectRes = dbCursor.fetchall()
        if selectRes != None:
            for date in selectRes:
                dateInDBList.append(date)       
    except Exception:
            logger.error("error occured\r\n"+traceback.format_exc())
            return
    if lastTradeDate in dateInDBList:
        #判断最近一个交易日是否在list里面，如果在则不查询，提高性能。
        logger.debug("stock:"+stockcode+" data is already at :"+lastTradeDate)
        return 
    df_cq =  ak.stock_zh_a_hist(symbol=stockcode[2:], adjust='',start_date=startdate,end_date=enddate)
    df_hfq = ak.stock_zh_a_hist(symbol=stockcode[2:], adjust='hfq',start_date=startdate,end_date=enddate)
    '''
        日期        开盘   收盘   最高   最低    成交量       成交额   振幅 涨跌幅 涨跌额 换手率
0     1991-04-03  -0.97  -0.97  -0.97  -0.97        1  5.000000e+03  0.00  4.90  0.05  0.00
1     1991-04-04  -0.97  -0.97  -0.97  -0.97        3  1.500000e+04  0.00  0.00  0.00  0.00
2     1991-04-05  -0.97  -0.97  -0.97  -0.97        2  1.000000e+04  0.00  0.00  0.00  0.00
3     1991-04-06  -0.97  -0.97  -0.97  -0.97        7  3.400000e+04  0.00  0.00  0.00  0.00
4     1991-04-08  -0.97  -0.97  -0.97  -0.97        2  1.000000e+04  0.00  0.00  0.00  0.00
...          ...    ...    ...    ...    ...      ...           ...   ...   ...   ...   ...
7621  2023-03-06  14.30  13.85  14.30  13.72  1455824  2.023955e+09  4.06 -3.08 -0.44  0.75
7622  2023-03-07  13.85  13.69  14.10  13.65  1279266  1.773655e+09  3.25 -1.16 -0.16  0.66
7623  2023-03-08  13.63  13.53  13.64  13.40  1096898  1.479839e+09  1.75 -1.17 -0.16  0.57
7624  2023-03-09  13.54  13.20  13.58  13.13  1736065  2.305766e+09  3.33 -2.44 -0.33  0.89
7625  2023-03-10  13.00  13.14  13.27  13.00   856996  1.128558e+09  2.05 -0.45 -0.06  0.44
    '''
    logger.debug(df_cq.to_string)
    logger.debug(df_hfq.to_string)
    if len(df_cq) != len(df_hfq):
        #两个长度不一致返回异常，下面for循环使用同一个索引
        logger.error('the stock:'+str(stockcode)+',df_cq length:'+str(len(df_cq))+' and df_hfq length:'+str(len(df_hfq))+',not same and return')
    for i in range(0,len(df_cq.index)):
        date = df_cq['日期'][i]
        if date in dateInDBList:
            logger.debug("date:"+date+" is in db and continue")
            continue
        if date in dealDuplicate:
            #ak数据会有同一天的重复数据，去重,这里对两个df进行遍历，理论上len一致，重复的时候应该两个df都重复
            logger.info('df data has duplicate date and ignore')
            continue
        dealDuplicate.append(date) 
        
        open_cq = dataFormat(df_cq['开盘'][i],2)
        close_cq = dataFormat(df_cq['收盘'][i],2)
        high_cq = dataFormat(df_cq['最高'][i],2)
        low_cq = dataFormat(df_cq['最低'][i],2)

        open_hfq = dataFormat(df_hfq['开盘'][i],2)
        close_hfq = dataFormat(df_hfq['收盘'][i],2)
        high_hfq = dataFormat(df_hfq['最高'][i],2)
        low_hfq = dataFormat(df_hfq['最低'][i],2)        


        volume = str(df_cq['成交量'][i])   #这个获取方法的成交量为手
        turnover = dataFormat(df_cq['成交额'][i],2)
        amplitude = dataFormat(df_cq['振幅'][i],2) 
        change_rate = dataFormat(df_cq['涨跌幅'][i],2)
        turnover_rate = dataFormat(df_cq['换手率'][i],2) #这个换手率是百分数
        logger.debug('开盘(cq):'+open_cq+',收盘(cq):'+close_cq+',最高(cq):'+high_cq+',最低(cq):'
            +low_cq+',开盘(hfq):'+open_hfq+',收盘(hfq):'+close_hfq+',最高(hfq):'+high_hfq+',最低(hfq):'
            +low_hfq+',成交量:'+volume+',成交额:'+turnover+',振幅:'+amplitude+',涨跌幅:'+change_rate+',换手率:'+turnover_rate)
        if len(open_cq) > 7 or len(open_hfq) > 9:
            logger.error('length of open exceed and exit,value:'+str(open_cq)+' '+str(open_hfq))
        
        try:
            #后面要扩展数据库表，扩展后直接清表，扩展这里的sql语句，重新跑即可。
            cmd = "insert into "+stockcode+" (date,open_cq,high_cq,low_cq,close_cq,open_hfq,high_hfq,low_hfq,close_hfq,volume,turnover,amplitude,change_rate,turnover_rate) VALUE (\""\
                +date+"\","+open_cq+","+high_cq+","+low_cq+","+close_cq+","+open_hfq+","+high_hfq+","+low_hfq+","+close_hfq+","+volume+","+turnover+","+amplitude+","+change_rate+","+turnover_rate+");"
            logger.debug("SQL:"+cmd)
            dbcursor.execute(cmd)
        except Exception:
            logger.error(traceback.format_exc())
            break
    return 
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
    cursor = db.cursor()
    return cursor
def slowloop(mem):
    #采集股票全量信息，维护近三年的股票数据。2020年后。
    while True:
        
        dbcursor = getDBCursor()
        if  dbcursor == None:
            exit(0)
        stockList = open('./stockList_rundata.txt','r')
        for stockcode in stockList:
            updateSingleStockData(stockcode,dbcursor)
        logger.info('do slow loop')
        time.sleep(1)  #避免故障场景循环过快
    pass

if __name__ == '__main__':
    if not initEnv():
        exit(0)
    slowloop()
    
    
    