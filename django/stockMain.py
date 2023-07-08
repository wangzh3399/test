import traceback
import datetime
import time
import akshare as ak
import decimal
from  basicfunc import *
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wxcloudrun.settings") 
django.setup()

from django.apps import apps
from updateStockLIist import *
from django.db import models
import wxcloudrun.models as mdl
from operator import attrgetter

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

def updateSingleStockData(stockcode,startdate,enddate):
    stockcode = fmtStockCode(stockcode,prefix=False)
    logger.info(enddate)
    try:
        stockModel = apps.get_app_config('wxcloudrun').get_model('stock_'+fmtStockCode(stockcode,prefix=False))

        #get_or_create会返回一个tuple,第一个值是查到或者创建的数据，第二个值是一个布尔，表示是否执行了创建操作。创建为True，未创建为False
        defaultUser = apps.get_app_config('wxcloudrun').get_model('usermanager').objects.get_or_create(userid="default")[0]
    except:
        logger.error(traceback.format_exc())
        return
    dealDuplicate = []
    #if not table_exists('wxcloudrun_stockdata_'+stockcode):   这个方法担心会有性能问题，用getModel判断异常    后面再看下https://www.cnblogs.com/hunterxiong/p/17262727.html
    #有三种思路：1) 使用exists   2）查询出来一个queryset然后判断是否在queryset中   3）使用try: get except:插入   根据chatgpt给的结论，使用主键冲突更能   4）get_or_create，get_or_create 是原子的，也就是说只要判断的数据使用 unique=True 定义模型节课避免重复插入 
    df_cq =  ak.stock_zh_a_hist(symbol=stockcode, adjust='',start_date=startdate,end_date=enddate)
    df_hfq = ak.stock_zh_a_hist(symbol=stockcode, adjust='hfq',start_date=startdate,end_date=enddate)
    logger.info(str(df_cq))
    '''
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
    for i in range(0,len(df_cq.index)):
        date = df_cq['日期'][i]
        if date in dealDuplicate:
            #ak数据会有同一天的重复数据，去重,这里对两个df进行遍历，理论上len一致，重复的时候应该两个df都重复
            logger.info('df data has duplicate date and ignore')
            continue
        dealDuplicate.append(date)
        if len(dataFormat(df_cq['开盘'][i],2)) > 7 or len(dataFormat(df_hfq['开盘'][i],2)) > 9:
            #我大A，应该不至于有这么高的价格。。
            logger.error('length of open exceed and exit,value:'+str(dataFormat(df_cq['开盘'][i],2))+' '+str(dataFormat(df_hfq['开盘'][i],2)))

        try:
            #date存在则会直接返回，不存在则使用default创建
            stock_data, created = stockModel.objects.get_or_create(date=date, defaults={
            'open_cq': dataFormat(df_cq['开盘'][i],2),
            'high_cq': dataFormat(df_cq['最高'][i],2),
            'low_cq': dataFormat(df_cq['最低'][i],2),
            'close_cq': dataFormat(df_cq['收盘'][i],2),
            'open_hfq': dataFormat(df_hfq['开盘'][i],2),
            'high_hfq': dataFormat(df_hfq['最高'][i],2),
            'low_hfq': dataFormat(df_hfq['最低'][i],2),
            'close_hfq': dataFormat(df_hfq['收盘'][i],2),
            'volume': str(df_cq['成交量'][i]),   #这个获取方法的成交量为手
            'turnover': dataFormat(df_cq['成交额'][i],2),
            'amplitude': dataFormat(df_cq['振幅'][i],2), 
            'change_rate': dataFormat(df_cq['涨跌幅'][i],2),
            'turnover_rate': dataFormat(df_cq['换手率'][i],2), #这个换手率是百分数
            'userid':defaultUser
        })
            if created:
                logger.debug("Successfully inserted record for date:", date)
            else:
                logger.debug("Record for date:", date, "already exists in the database")
        except Exception:
            logger.error(traceback.format_exc())
            logger.error(f'''
            'open_cq': {dataFormat(df_cq['开盘'][i],2)},
            'high_cq': {dataFormat(df_cq['最高'][i],2)},
            'low_cq': {dataFormat(df_cq['最低'][i],2)},
            'close_cq': {dataFormat(df_cq['收盘'][i],2)},
            'open_hfq': {dataFormat(df_hfq['开盘'][i],2)},
            'high_hfq': {dataFormat(df_hfq['最高'][i],2)},
            'low_hfq': {dataFormat(df_hfq['最低'][i],2)},
            'close_hfq': {dataFormat(df_hfq['收盘'][i],2)},
            'volume': {str(df_cq['成交量'][i])},
            'turnover': {dataFormat(df_cq['成交额'][i],2)},
            'amplitude': {dataFormat(df_cq['振幅'][i],2)}, 
            'change_rate': {dataFormat(df_cq['涨跌幅'][i],2)},
            'turnover_rate': {dataFormat(df_cq['换手率'][i],2)},
            'userid':{defaultUser}'''
            )
            break
    return 

if __name__ == '__main__':
    #后台独立运行的进程，持续更新stock数据，维护自2020年以后的数据，多进程  还有个问题，每次django启动，应该是会把model加载到apps里面去。如果动态生成，下次重新运行时，如果apps里少了某个models会认为delete了，比如createStockmodel 0001  然后第二次执行0002，会认为是把0001改名为0002

    stocks = mdl.stockbasicinfo.objects.all()
    for i in stocks:
        logger.info('start update stockcode:'+i.stockcode)
        updateSingleStockData(i.stockcode,"20200101",datetime.datetime.now().strftime("%Y%m%d"))
        logger.info('finished update stockcode:'+i.stockcode)

