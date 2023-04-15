import pandas as pd
import akshare as ak
from basicfunc import *
#import django
from django.apps import apps
from models_generate import *
import time
import wxFrontEnd
##from django.db import connection, migrations, models
#from django.db.migrations.executor import MigrationExecutor
#import os
 
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wxcloudrun.settings')
#django.setup()
#http://www.360doc.com/content/22/0120/16/35291147_1014183755.shtml  策略可以参考这个.
#策略思路1：选TOP1行业，选龙头，做多.  有些策略需要结合前一天或几天的数据
class monitorStrategy(): #定义一个基础类
    def __init__(self,stockCode):
        self.stockCode = stockCode
        self.userlist = []
        self.strategyAbbrName = ''   #abbreviation
        self.strategyName = ''
        self.curPrice = 0
        #交易日当天价格
        self.open = 0
        self.low = 0
        self.high = 0
        self.dma5 = 0    #MA5，当天结合股价动态更新
        self.dma10 = 0   #MA10，当天结合股价动态更新
        self.dma20 = 0    #MA5，当天结合股价动态更新
        self.dma30 = 0   #MA10，当天结合股价动态更新
        #交易日前一天数据  pre1
        self.pre1open = 0   #前一个交易日开盘价
        self.pre1high = 0   #前一个交易日盘中最高
        self.pre1low = 0    #前一个交易日盘中最低
        self.pre1close = 0    #前一个交易日收盘
        self.pre1dsum4 = 0    #前1天统计的前4天收盘价和
        self.pre1dma5 = 0  #前一天统计的dma5
        self.pre1dsum9 = 0    #前一天统计的前9天收盘价和
        self.pre1dma10 = 0 #前一天统计的dma10
        self.pre1dsum19 = 0    #前一天统计的前19天收盘价和
        self.pre1dma20 = 0 #前一天统计的dma20
        self.pre1dsum29 = 0    #前一天统计的前29天收盘价和
        self.pre1dma30 = 0    #前一天统计的dma20
        #交易日前两天数据  pre2
        self.pre2dsum4 = 0
        self.pre2dsum9 = 0
        self.pre2dsum19 = 0
        self.pre2dsum29 = 0
        
class monitorY1C4XStrategy(monitorStrategy):
    #需要一个参考backtrader做回测
    def __init__(self,stockCode):
        self.strategyAbbrName = 'Y1C4X01'   #abbreviation
        self.strategyName = '一阳穿四线01'
        self.stockCode = stockcodeDelPrefix(stockCode)
        self.stockdf = pd.DataFrame(columns=['time','number'])  #暂时定义为分钟级
        self.dateofMonitor = datetime.datetime.now().strftime('%Y-%m-%d')
        self.stockModel = getModel('wxcloudrun_stockdata_'+self.stockCode,'wxcloudrun')
        #self.stockQuerySet = self.stockModel.objects.filter()
        self.dsum4 = self.stockCode
        self.tradeList = ak.tool_trade_date_hist_sina()['trade_date'].tolist()
        self.tradeDate = datetime.datetime.now().strftime('%Y-%m-%d')
        self.isTradeDay = True if self.tradeDate in self.tradeList else False

        #交易条件
        self.conditionHighPriceCrossMa5Ma10 = 0  #前一天最高价上穿MA5  MA10
    def judgeCondition(self):
        #当天上穿后回落，第二天开盘价MA5上穿MA10
        df = ak.stock_zh_a_hist_min_em(symbol=self.stockCode, start_date=self.tradeDate+' 09:15:00', end_date=self.tradeDate+' 15:30:00', period='1', adjust='')
        '''
                 时间     开盘   收盘   最高   最低  成交量    成交额    最新价
0   2023-04-06 09:30:00  35.44  35.44  35.44  35.44  16479   58401576.0  35.440
1   2023-04-06 09:31:00  35.40  35.59  35.59  35.30  37001  131121097.0  35.438
2   2023-04-06 09:32:00  35.60  35.40  35.68  35.36  16976   60323698.0  35.461
3   2023-04-06 09:33:00  35.37  35.65  35.65  35.37  16852   59789351.0  35.464
4   2023-04-06 09:34:00  35.65  35.70  35.75  35.58   9911   35354874.0  35.486
        '''
        self.curPrice = df['收盘'][-1]
        self.open = df['开盘'][0]
        self.opendma5 = (self.pre1dsum4 + self.open) / 5
        self.dma5 = (self.pre1dsum4 + self.curPrice) / 5
        self.opendma10 = (self.pre1dsum9 + self.open) / 10
        self.dma10 = (self.pre1dsum9 + self.curPrice) / 10
        if self.opendma5 > self.opendma10
            self.noticeUser('[Strategy notices]:'+self.stockCode +' is time to buy in for openMA5['+str(self.opendma5)+'] cross up openMA10['+str(self.opendma10)+']')
        if self.dma5 > self.dma10:
            self.noticeUser('[Strategy notices]:'+self.stockCode +' is time to buy in for MA5['+str(self.dma5)+'] cross up MA10['+str(self.dma10)+']')
    def noticeUser(self,msg):
        for userid in self.userlist:
            wxFrontEnd.messageSend.sendmsg(userid,msg)
        pass
    def getPreTradeDate(self,date):
        preTradeDay = datetime.datetime.fromtimestamp (date.timestamp() - 86400).strftime('%Y-%m-%d')
        while preTradeDay not in self.tradeList:
            preTradeDay = datetime.datetime.fromtimestamp (preTradeDay.timestamp() - 86400).strftime('%Y-%m-%d')
        return  preTradeDay    
    def monitorLoop(self):
        while True:
            nowdate = datetime.datetime.now()
            if nowdate.hour in [9,10,11,13,14]:
                if self.judgeCondition():
                    self.noticeUser()
                else:
                    time.sleep(60)   #这里间隔如果太短可能会被封，后面要考虑优化请求间隔。
            else:
                #每天8点,更新基础数据
                if nowdate.hour == 8:
                    
                    #判断当天是否交易日
                    self.isTradeDay = True if datetime.datetime.now().strftime('%Y-%m-%d') in self.tradeList else False

                    #获取上一个交易日
                    pre1TradeDay = self.getPreTradeDate(nowdate)
                    try:
                        pre1stockQuerySet = self.stockModel.objects.get(date=pre1TradeDay)
                    except:
                        pre1stockQuerySet = None
                    if pre1stockQuerySet == None:
                        logger.error('pre1TradeDay stockdata not exists:'+pre1TradeDay)
                        self.alarmManager('pre1TradeDay stockdata not exists:'+pre1TradeDay)
                        exit(0)
                    self.pre1dsum4 = pre1stockQuerySet.dsum4
                    self.pre1dsum9 = pre1stockQuerySet.dsum9
                    self.pre1dsum19 = pre1stockQuerySet.dsum19
                    self.pre1dsum29 = pre1stockQuerySet.dsum29
                    self.pre1open = pre1stockQuerySet.open_cq
                    self.pre1high = pre1stockQuerySet.high_cq
                    self.pre1low = pre1stockQuerySet.low_cq
                    self.pre1close = pre1stockQuerySet.close_cq

                    pre2TradeDay = self.getPreTradeDate(pre1TradeDay)
                    try:
                        pre2stockQuerySet = self.stockModel.objects.get(date=pre2TradeDay)
                    except:
                        pre2stockQuerySet = None
                    if pre2stockQuerySet == None:
                        logger.error('pre2TradeDay stockdata not exists:'+pre2TradeDay)
                        self.alarmManager('pre2TradeDay stockdata not exists:'+pre2TradeDay)
                        exit(0)
                    self.pre2dsum4 = pre2stockQuerySet.dsum4
                    self.pre2dsum9 = pre2stockQuerySet.dsum9
                    self.pre2dsum19 = pre2stockQuerySet.dsum19
                    self.pre2dsum29 = pre2stockQuerySet.dsum29
                    self.conditionHighPriceCrossMa5Ma10 = True if (self.pre2dsum4 + self.pre1high)/5 > (self.pre2dsum9 + self.pre1high)/10 else False
            datetime.datetime.now()
