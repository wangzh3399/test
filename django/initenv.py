import logging
import pymysql
import configparser
import traceback
import pathlib 
import sys
import os
FILE = pathlib.Path(__file__).absolute()
# 加入 main.py所在文件夹路径
ROOT = FILE.parents[0] 

if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))
    sys.path.insert(0, str(ROOT))

from basicfunc import *
from models_generate import *
from updateStockLIist import *

#这个脚本手动执行，执行清理环境并重构环境。

def buildStockTable(dbCursor):
    
    pass
def buildStockStaticData(dbCursor):
    #不check表是否存在，默认环境已经生成表。这里默认先使用基础表添加股票信息，再由updateStockListPerDay来负责增量更新。
    stockFile = open('./stocklist.txt','r')
    #for stock in stockFile:
def initEnv():
    #更新股票list，每个周六定时执行。
    logger.info('init envir')
    dbCursor = getDBConn().cursor()
    #启动时检查数据库完整性、表结构完整性，不完整则退出
    if dbCursor == None:
        exit(0)
    if buildStockTable(dbCursor) == None:
        exit(0)
    if buildStockStaticData(dbCursor) == None:
        exit(0)
    logger.info('init envir successfully')
    return 0


if __name__ == '__main__':
    #initEnv()
    #不论如何，执行这个脚本时，尝试删除Stock数据库并重建。
    #os.system('mariadb -h localhost -proot -A -e "drop database Stock"')
    #os.system('mariadb -h localhost -proot -A -e "create database Stock  character set utf8"')
    create_table('usermanager','wxcloudrun')
    
    #updateStockListPerDay()