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


from basicfunc import *


#盯盘：1）板块盯盘   2）制定股票列表盯盘。   可以后续打通前一天的策略选股导入

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
def monitorStock(monitorObj):  #monitorObj: 每一个策略obj，独立一个策略类的对象，包含类的存储数据
    pass
def runMonitor():
    #采集股票基础信息,分时信息监控，先放内存里吧，不入库
    while True:
        
        dbConn = getDBConn()
        if  dbConn == None:
            exit(0)
        selectStockCmd = 'select stockcode from wxcloudrun_strategyConfig where monitorStrategy="quick"';  #快策略股票
        dbCursor = dbConn.cursor()
        dbCursor.exec(selectStockCmd)
        selectRes = dbCursor.fetchall()
        dbConn.close()
        if selectRes == None:
            logger.error('wxcloudrun_strategyConfig empty,pls build strategy first!')
            exit(0)
        for res in selectRes:
            monitorStock()
if __name__ == '__main__':
    if not initEnv():
        exit(0)
    #mem = buildShareMem()
    #quick依赖slow的数据库表更新，可以一起拉起，但如果数据库表信息为空，则等待。
    runMonitor()
    
    
    