import logging
import traceback
import datetime
import time
import akshare as ak
import decimal
from  basicfunc import *
from models_generate import *
from django.apps import apps
from updateStockLIist import *

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

def getDMA(df,curIndex,ma):  #算ma时，要包含当天的数据。
    if curIndex - ma + 1 <0:   # 当取第5天数据时index为4，偏移5，则4-5+1 要>=0
        return 0
    sum = 0
    while ma > 0 :
        sum = sum + df['收盘'][curIndex-ma+1]
        ma = ma - 1
    return sum/ma
def getWMA(df,curIndex,ma):  #算ma时，要包含当天的数据。   有节假日要考虑，这个方法不行。
    curDate = df['date'][curIndex]
    dt = datetime.datetime.strptime(curDate, '%Y-%m-%d')
    shift1 = dt.isoweekday() + 2   #weeday这里没有周六或者周日。如果是周五，那上一周偏移是7 ，周四，则偏移是6
    shift2 = shift1 + 5
    shift3 = shift2 + 5 
    shift4 = shift3 + 5
    if curIndex < shift1 + shift2 + shift3 + shift4:
        return 0 
    if curIndex - shiftday + 1 <0:   # 当取第5天数据时index为4，偏移5，则4-5+1 要>=0
        return 0
    sum = 0
    while shiftday > 0 :
        sum = sum + df['收盘'][curIndex-shiftday+1]
        shiftday = shiftday - 1
    return sum/shiftday
def getMMA(df,dffield,curIndex,shiftday):  #算ma时，要包含当天的数据。
    if curIndex - shiftday + 1 <0:   # 当取第5天数据时index为4，偏移5，则4-5+1 要>=0
        return 0
    sum = 0
    while shiftday > 0 :
        sum = sum + df[dffield][curIndex-shiftday+1]
        shiftday = shiftday - 1
    return sum/shiftday

def updateSingleStockData(stockcode):
    #维护近三年的股票数据. stockcode 默认带sz sh等前缀
    t = datetime.datetime.now()
    month = '0' + str(t.month)
    day = '0' + str(t.day)
    startdate = str(t.year-3)+month[len(month)-2:]+day[len(day)-2:]
    enddate = str(t.year)+month[len(month)-2:]+day[len(day)-2:]
    #lastTradeDate = getLastTradeDate()
    dealDuplicate = []
    #if not table_exists('wxcloudrun_stockdata_'+stockcode):   这个方法担心会有性能问题，用getModel判断异常    后面再看下https://www.cnblogs.com/hunterxiong/p/17262727.html
    #有三种思路：1) 使用exists   2）查询出来一个queryset然后判断是否在queryset中   3）使用try: get except:插入   根据chatgpt给的结论，使用主键冲突更能   4）get_or_create，get_or_create 是原子的，也就是说只要判断的数据使用 unique=True 定义模型节课避免重复插入 
    try:
        #获取不到则说明没有建表
        stockModel = getModel(tableName='wxcloudrun_stockdata_'+stockcode,appLabel='wxcloudrun')
    except:    
        create_table()
    stockModel = getModel(tableName='wxcloudrun_stockdata_'+stockcode,appLabel='wxcloudrun')
    #queryUserList = stockModel.objects.all()

    df_cq =  ak.stock_zh_a_hist(symbol=stockcode, adjust='',start_date=startdate,end_date=enddate)
    df_hfq = ak.stock_zh_a_hist(symbol=stockcode, adjust='hfq',start_date=startdate,end_date=enddate)
    '''
    if len(queryUserList) > 0 :
        logger.info('lastTradeData'+lastTradeDate+' is already in DBTable')
        return

    #stockcode默认无前缀     这里日期如何插入还需要考虑下，去重等场景。

    
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
    if len(df_cq) != len(df_hfq):
        #两个长度不一致返回异常，下面for循环使用同一个索引
        logger.error('the stock:'+str(stockcode)+',df_cq length:'+str(len(df_cq))+' and df_hfq length:'+str(len(df_hfq))+',not same and return')
    weekPriceList = []   #用于存储当周最后一日date
    monthPriceList = []   #用于存储当月最后一日date
    for i in range(0,len(df_cq.index)):
        date = df_cq['日期'][i]
        dealDuplicate.append(date)
        isTailOfMonth = False
        if date in dealDuplicate:
            #ak数据会有同一天的重复数据，去重,这里对两个df进行遍历，理论上len一致，重复的时候应该两个df都重复
            logger.info('df data has duplicate date and ignore')
            continue
        if len(dataFormat(df_cq['开盘'][i],2)) > 7 or len(dataFormat(df_hfq['开盘'][i],2)) > 9:
            #我大A，应该不至于有这么高的价格。。
            logger.error('length of open exceed and exit,value:'+str(dataFormat(df_cq['开盘'][i],2))+' '+str(dataFormat(df_hfq['开盘'][i],2)))
        #判断周几，如果小于上一个日期的周几，则判定为上周结束了。有一个情况就是过年或其他特殊情况，跨超过1周的休假。那么要判断上下周日期只差不大于5
        if i < len(df_cq.index) - 1:
            nextdate = df_cq['日期'][i+1]

            #判断月份
            if date.split('-')[1] != nextdate.split('-')[1]:
                monthPriceList.append(float(df_cq['收盘'][i]))
                isTailOfMonth = True
            dt = datetime.datetime.strptime(date, '%Y-%m-%d')
            dtnext = datetime.datetime.strptime(nextdate, '%Y-%m-%d')
            if dtnext.timestamp() - dt.timestamp() > 6:  
                #特殊情况就是过年或其他特殊情况，跨超过1周的休假。1 2 3 4 5 [6] [7] 1 2 3 4 5  上下间隔超过6天，即≥7天即可认为上一个date是上周的最后一天。拿时间戳算是按7天。
                
                weekPriceList.append(float(df_cq['收盘'][i]))
            elif dtnext.isoweekday() < dt.isoweekday():
                #间隔小于一周，不会出现后一天的weekday大于前一天，且跨周。所以当后一天小于前一天，说明到下一周了,把上一周入list
                weekPriceList.append(float(df_cq['收盘'][i]))
            else:
                #当周还未结束，do nothing
                pass


        wsum4,wsum9,wsum19,wsum29,msum4,msum9,msum19,msum29,wma5,wma10,wma20,wma30,mma5,mma10,mma20,mma30 = 0,0,0,0,0,0,0,0,0,0,0,0
        #周均线
        if len(weekPriceList) >= 4:
            #当前先按除权计算均线，后面如果有问题再说。研究了半天，发现实际使用的均线基本还是按照这个来参考的。
            #如果当前记录是周五，wsum4刚好算今天，上面weekPriceList已经append了。wma5
            wsum4 = weekPriceList[-1] + weekPriceList[-2] + weekPriceList[-3] + weekPriceList[-4]
            if dt.isoweekday() != 5:
                wma5 = (weekPriceList[-1] + weekPriceList[-2] + weekPriceList[-3] + weekPriceList[-4] + float(dataFormat(df_cq['收盘'][i],2)))/5
        if len(weekPriceList) >= 5 and dt.isoweekday() == 5:
            #如果是周五，则wma5，直接取近5个数据平均。否则去近4个+当天求平均
            wma5 = (weekPriceList[-1] + weekPriceList[-2] + weekPriceList[-3] + weekPriceList[-4] + weekPriceList[-5])/5
            
        if len(weekPriceList) >= 9:
            wsum9 = weekPriceList[-1] + weekPriceList[-2] + weekPriceList[-3] + weekPriceList[-4]\
                + weekPriceList[-5] + weekPriceList[-6] + weekPriceList[-7] + weekPriceList[-8] + weekPriceList[-9]
            if dt.isoweekday() != 5:
                wma10 = (weekPriceList[-1] + weekPriceList[-2] + weekPriceList[-3] + weekPriceList[-4]
                    + weekPriceList[-5] + weekPriceList[-6] + weekPriceList[-7] + weekPriceList[-8] + weekPriceList[-9] + float(dataFormat(df_cq['收盘'][i],2)))/10
        if len(weekPriceList) >= 10 and dt.isoweekday() == 5:
            wma10 = (weekPriceList[-1] + weekPriceList[-2] + weekPriceList[-3] + weekPriceList[-4]
                + weekPriceList[-5] + weekPriceList[-6] + weekPriceList[-7] + weekPriceList[-8] + weekPriceList[-9] + + weekPriceList[-10])/10

        if len(weekPriceList) >= 19 :
            wsum19 = weekPriceList[-1] + weekPriceList[-2] + weekPriceList[-3] + weekPriceList[-4]\
                 + weekPriceList[-5] + weekPriceList[-6] + weekPriceList[-7] + weekPriceList[-8] + weekPriceList[-9]\
                 + weekPriceList[-10] + weekPriceList[-11] + weekPriceList[-12] + weekPriceList[-13] + weekPriceList[-14]\
                 + weekPriceList[-15] + weekPriceList[-16] + weekPriceList[-17] + weekPriceList[-18] + weekPriceList[-19]
            if dt.isoweekday() != 5 :
                wma20 = (weekPriceList[-1] + weekPriceList[-2] + weekPriceList[-3] + weekPriceList[-4]
                    + weekPriceList[-5] + weekPriceList[-6] + weekPriceList[-7] + weekPriceList[-8] + weekPriceList[-9]
                    + weekPriceList[-10] + weekPriceList[-11] + weekPriceList[-12] + weekPriceList[-13] + weekPriceList[-14]
                    + weekPriceList[-15] + weekPriceList[-16] + weekPriceList[-17] + weekPriceList[-18] + weekPriceList[-19] + float(dataFormat(df_cq['收盘'][i],2)))/20
        if len(weekPriceList) >= 20 and dt.isoweekday() == 5 :
            wma20 = (weekPriceList[-1] + weekPriceList[-2] + weekPriceList[-3] + weekPriceList[-4]
                 + weekPriceList[-5] + weekPriceList[-6] + weekPriceList[-7] + weekPriceList[-8] + weekPriceList[-9]
                 + weekPriceList[-10] + weekPriceList[-11] + weekPriceList[-12] + weekPriceList[-13] + weekPriceList[-14]
                 + weekPriceList[-15] + weekPriceList[-16] + weekPriceList[-17] + weekPriceList[-18] + weekPriceList[-19] + weekPriceList[-20] )/20
        if len(weekPriceList) >= 29 :
            wsum29 = weekPriceList[-1] + weekPriceList[-2] + weekPriceList[-3] + weekPriceList[-4]\
                + weekPriceList[-5] + weekPriceList[-6] + weekPriceList[-7] + weekPriceList[-8] + weekPriceList[-9]\
                + weekPriceList[-10] + weekPriceList[-11] + weekPriceList[-12] + weekPriceList[-13] + weekPriceList[-14]\
                + weekPriceList[-15] + weekPriceList[-16] + weekPriceList[-17] + weekPriceList[-18] + weekPriceList[-19]\
                + weekPriceList[-20] + weekPriceList[-21] + weekPriceList[-22] + weekPriceList[-23] + weekPriceList[-24]\
                + weekPriceList[-25] + weekPriceList[-26] + weekPriceList[-27] + weekPriceList[-28] + weekPriceList[-29]
            if dt.isoweekday() != 5:
                wma30 = (weekPriceList[-1] + weekPriceList[-2] + weekPriceList[-3] + weekPriceList[-4]
                    + weekPriceList[-5] + weekPriceList[-6] + weekPriceList[-7] + weekPriceList[-8] + weekPriceList[-9]
                    + weekPriceList[-10] + weekPriceList[-11] + weekPriceList[-12] + weekPriceList[-13] + weekPriceList[-14]
                    + weekPriceList[-15] + weekPriceList[-16] + weekPriceList[-17] + weekPriceList[-18] + weekPriceList[-19]
                    + weekPriceList[-20] + weekPriceList[-21] + weekPriceList[-22] + weekPriceList[-23] + weekPriceList[-24]
                    + weekPriceList[-25] + weekPriceList[-26] + weekPriceList[-27] + weekPriceList[-28] + weekPriceList[-29] + float(dataFormat(df_cq['收盘'][i],2)))/30
        if len(weekPriceList) >= 30 and dt.isoweekday() == 5 :
            wma30 = (weekPriceList[-1] + weekPriceList[-2] + weekPriceList[-3] + weekPriceList[-4]
                + weekPriceList[-5] + weekPriceList[-6] + weekPriceList[-7] + weekPriceList[-8] + weekPriceList[-9]
                + weekPriceList[-10] + weekPriceList[-11] + weekPriceList[-12] + weekPriceList[-13] + weekPriceList[-14]
                + weekPriceList[-15] + weekPriceList[-16] + weekPriceList[-17] + weekPriceList[-18] + weekPriceList[-19]
                + weekPriceList[-20] + weekPriceList[-21] + weekPriceList[-22] + weekPriceList[-23] + weekPriceList[-24]
                + weekPriceList[-25] + weekPriceList[-26] + weekPriceList[-27] + weekPriceList[-28] + weekPriceList[-29] + weekPriceList[-30] )/30
        #月均线       
        if len(monthPriceList) >= 4:
            #当前先按除权计算均线，后面如果有问题再说。研究了半天，发现实际使用的均线基本还是按照这个来参考的.
            msum4 = monthPriceList[-1] + monthPriceList[-2] + monthPriceList[-3] + monthPriceList[-4]
            if not isTailOfMonth :
                mma5 = (monthPriceList[-1] + monthPriceList[-2] + monthPriceList[-3] + monthPriceList[-4] + float(dataFormat(df_cq['收盘'][i],2)))/5
        if len(monthPriceList) >= 5 and isTailOfMonth:
            mma5 = (monthPriceList[-1] + monthPriceList[-2] + monthPriceList[-3] + monthPriceList[-4] + monthPriceList[-5])/5

        if len(monthPriceList) >= 9:
            msum9 = monthPriceList[-1] + monthPriceList[-2] + monthPriceList[-3] + monthPriceList[-4]\
                + monthPriceList[-5] + monthPriceList[-6] + monthPriceList[-7] + monthPriceList[-8] + monthPriceList[-9]
            if  not isTailOfMonth :
                mma10 = (monthPriceList[-1] + monthPriceList[-2] + monthPriceList[-3] + monthPriceList[-4]
                    + monthPriceList[-5] + monthPriceList[-6] + monthPriceList[-7] + monthPriceList[-8] + monthPriceList[-9]+ float(dataFormat(df_cq['收盘'][i],2)))/10
        if len(monthPriceList) >= 10 and isTailOfMonth:
            mma10 = (monthPriceList[-1] + monthPriceList[-2] + monthPriceList[-3] + monthPriceList[-4]
                + monthPriceList[-5] + monthPriceList[-6] + monthPriceList[-7] + monthPriceList[-8] + monthPriceList[-9]+ monthPriceList[-10])/10

        if len(monthPriceList) >= 19:
            msum19 = monthPriceList[-1] + monthPriceList[-2] + monthPriceList[-3] + monthPriceList[-4]\
                + monthPriceList[-5] + monthPriceList[-6] + monthPriceList[-7] + monthPriceList[-8] + monthPriceList[-9]\
                + monthPriceList[-10] + monthPriceList[-11] + monthPriceList[-12] + monthPriceList[-13] + monthPriceList[-14]\
                + monthPriceList[-15] + monthPriceList[-16] + monthPriceList[-17] + monthPriceList[-18] + monthPriceList[-19]
            if not isTailOfMonth :
                mma20 = (monthPriceList[-1] + monthPriceList[-2] + monthPriceList[-3] + monthPriceList[-4]
                    + monthPriceList[-5] + monthPriceList[-6] + monthPriceList[-7] + monthPriceList[-8] + monthPriceList[-9]    
                    + monthPriceList[-10] + monthPriceList[-11] + monthPriceList[-12] + monthPriceList[-13] + monthPriceList[-14]
                    + monthPriceList[-15] + monthPriceList[-16] + monthPriceList[-17] + monthPriceList[-18] + monthPriceList[-19] + float(dataFormat(df_cq['收盘'][i],2)))/20
        if len(monthPriceList) >= 20 and isTailOfMonth: 
            mma20 = (monthPriceList[-1] + monthPriceList[-2] + monthPriceList[-3] + monthPriceList[-4]
                + monthPriceList[-5] + monthPriceList[-6] + monthPriceList[-7] + monthPriceList[-8] + monthPriceList[-9]    
                + monthPriceList[-10] + monthPriceList[-11] + monthPriceList[-12] + monthPriceList[-13] + monthPriceList[-14]
                + monthPriceList[-15] + monthPriceList[-16] + monthPriceList[-17] + monthPriceList[-18] + monthPriceList[-19]+ monthPriceList[-20])/20

        if len(monthPriceList) >= 29:
            msum29 = monthPriceList[-1] + monthPriceList[-2] + monthPriceList[-3] + monthPriceList[-4]\
                + monthPriceList[-5] + monthPriceList[-6] + monthPriceList[-7] + monthPriceList[-8] + monthPriceList[-9]\
                + monthPriceList[-10] + monthPriceList[-11] + monthPriceList[-12] + monthPriceList[-13] + monthPriceList[-14]\
                + monthPriceList[-15] + monthPriceList[-16] + monthPriceList[-17] + monthPriceList[-18] + monthPriceList[-19]\
                + monthPriceList[-20] + monthPriceList[-21] + monthPriceList[-22] + monthPriceList[-23] + monthPriceList[-24]\
                + monthPriceList[-25] + monthPriceList[-26] + monthPriceList[-27] + monthPriceList[-28] + monthPriceList[-29]
            if not isTailOfMonth :
                mma30 = (monthPriceList[-1] + monthPriceList[-2] + monthPriceList[-3] + monthPriceList[-4]
                    + monthPriceList[-5] + monthPriceList[-6] + monthPriceList[-7] + monthPriceList[-8] + monthPriceList[-9]    
                    + monthPriceList[-10] + monthPriceList[-11] + monthPriceList[-12] + monthPriceList[-13] + monthPriceList[-14]
                    + monthPriceList[-15] + monthPriceList[-16] + monthPriceList[-17] + monthPriceList[-18] + monthPriceList[-19]    
                    + monthPriceList[-20] + monthPriceList[-21] + monthPriceList[-22] + monthPriceList[-23] + monthPriceList[-24]                 
                    + monthPriceList[-25] + monthPriceList[-26] + monthPriceList[-27] + monthPriceList[-28] + monthPriceList[-29] + float(dataFormat(df_cq['收盘'][i],2)))/30
        if len(monthPriceList) >= 30 and isTailOfMonth:
            mma30 = (monthPriceList[-1] + monthPriceList[-2] + monthPriceList[-3] + monthPriceList[-4]
                + monthPriceList[-5] + monthPriceList[-6] + monthPriceList[-7] + monthPriceList[-8] + monthPriceList[-9]    
                + monthPriceList[-10] + monthPriceList[-11] + monthPriceList[-12] + monthPriceList[-13] + monthPriceList[-14]
                + monthPriceList[-15] + monthPriceList[-16] + monthPriceList[-17] + monthPriceList[-18] + monthPriceList[-19]    
                + monthPriceList[-20] + monthPriceList[-21] + monthPriceList[-22] + monthPriceList[-23] + monthPriceList[-24]                 
                + monthPriceList[-25] + monthPriceList[-26] + monthPriceList[-27] + monthPriceList[-28] + monthPriceList[-29]+ monthPriceList[-30])/30
        try:
            stock_data, created = stockModel.objects.get_or_create(date=date, defaults={
            'open_cq': dataFormat(df_cq['开盘'][i],2),
            'high_cq': dataFormat(df_cq['最高'][i],2),
            'low_cq': dataFormat(df_cq['最低'][i],2),
            'close_cq': dataFormat(df_cq['收盘'][i],2),
            'open_hfq': dataFormat(df_hfq['开盘'][i],2),
            'high_hfq': dataFormat(df_hfq['最高'][i],2),
            'low_hfq': dataFormat(df_hfq['最低'][i],2),
            'close_hfq': dataFormat(df_hfq['收盘'][i],2),
            'dsum4': dataFormat(getDMA(df_cq,i,4),2),   
            'dsum9': dataFormat(getDMA(df_cq,i,9),2),
            'dsum19': dataFormat(getDMA(df_cq,i,19),2),
            'dsum29': dataFormat(getDMA(df_cq,i,29),2), 
            'wsum4': wsum4, 
            'wsum9': wsum9,
            'wsum19': wsum19,
            'wsum29': wsum29,
            'msum4': msum4,
            'msum9': msum9,
            'msum19': msum19,
            'msum29': msum29,
            'dma5': dataFormat(getDMA(df_cq,i,5),2),  
            'dma10': dataFormat(getDMA(df_cq,i,10),2),
            'dma20': dataFormat(getDMA(df_cq,i,20),2),
            'dma30': dataFormat(getDMA(df_cq,i,30),2), 
            'wma5': wma5, 
            'wma10': wma10,
            'wma20': wma20,
            'wma30': wma30,
            'mma5': mma5,
            'mma10': mma10,
            'mma20': mma20,
            'mma30': mma30,
            'volume': str(df_cq['成交量'][i]),   #这个获取方法的成交量为手
            'turnover': dataFormat(df_cq['成交额'][i],2),
            'amplitude': dataFormat(df_cq['振幅'][i],2), 
            'change_rate': dataFormat(df_cq['涨跌幅'][i],2),
            'turnover_rate': dataFormat(df_cq['换手率'][i],2) #这个换手率是百分数
        })
            if created:
                logger.debug("Successfully inserted record for date:", date)
            else:
                logger.debug("Record for date:", date, "already exists in the database")
        except Exception:
            logger.error(traceback.format_exc())
            break
    return 
def slowloop():
    #采集股票全量信息，维护近三年的股票数据。2020年后。
    previousRunDay = 0  #同一天只执行1轮
    loopMonitor = 0   #用于监控异常处理，如果已经处理过一次异常，第二次就不再处理了直接退出。
    while True:
        if datetime.datetime.now().day == previousRunDay:
            time.sleep(60)
            continue
        else:
            previousRunDay = datetime.datetime.now().day
            updateStockListPerDay()  #每天更新一次数据库stock
        try:
            stockModel = getModel(tableName='wxcloudrun_stockstaticdata',appLabel='wxcloudrun')
        except:
            #这里抛异常应该是没有创建静态数据表，调用updateStockList来创建数据表并生成股票列表数据
            logger.error(traceback.format_exc())
            if loopMonitor > 0 :
                break
            else:
                updateStockListPerDay()  
                loopMonitor = loopMonitor + 1
        stocks = stockModel.objects.all()
        if len(stocks) == 0:
            logger.error('wxcloudrun_stockstaticdata empty,pls run initenv.py first!')
            updateStockListPerDay()
            stocks = stockModel.objects.all()
        for stock in stocks:
            updateSingleStockData(stock)
            logger.info('do slow loop')
            time.sleep(1)  #避免故障场景循环过快

if __name__ == '__main__':
    slowloop()
    
    
    