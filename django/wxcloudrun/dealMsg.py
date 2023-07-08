import wechatpy
from basicfunc import *
import traceback
import datetime
import sys
import re
from django.apps import apps

strategyList = ['1YC4X','fltp']  #1YC4X 一阳穿四线    fltp：放量突破

def filterReply(msg,content):
    #对于管理员放开调试，对于其他用户不放开.
    #公众号不能推荐敏感信息，要做好过滤。
    if 'FromUserName' not in msg._data.keys():
        logger.error('msg error, missing Event!')
        return '服务器内部错误,错误码'+str(sys._getframe().f_lineno)+',请联系管理员！'
    dbconn  = getDBConn()
    dbCursor = dbconn.cursor()
    try:
        selectCmd = 'select userid from wxcloudrun_usermanager where level="manager";'
        dbCursor.execute(selectCmd)
        selectRes = dbCursor.fetchall()
    except:
        logger.error('db error!\r\n'+traceback.format_exc())
        return '服务器内部错误,错误码'+str(sys._getframe().f_lineno)+',请联系管理员！'  
    if selectRes == None:
        logger.error('db error, missing manager!')
        return '服务器内部错误,错误码'+str(sys._getframe().f_lineno)+',请联系管理员！'   
    managerList = []
    for userid in selectRes:
        managerList.append(userid[0])
    if msg._data['FromUserName'] in managerList:
        #对于管理员，直接返回原始信息
        return content 
    if content.lower().find('error') != -1:
        return '服务器内部错误,错误码'+str(sys._getframe().f_lineno)+',请联系管理员！'
    else:
        return content

def checkUserValid(userid):  #检查用户id有效性
    userModel = getModel(tableName='wxcloudrun_usermanager',appLabel='wxcloudrun')
    queryUserList = userModel.objects.filter(userid=userid)
    if len(queryUserList) > 0 and queryUserList.valid:
        return True
    return False
def checkStockcodeValid(stockcode): #检查股票代码有效性
    stockStaticModel = getModel(tableName='wxcloudrun_stockstaticdata',appLabel='wxcloudrun')
    queryUserList = stockStaticModel.objects.filter(stockcode=stockcode)
    if len(queryUserList) > 0:
        return True
    return False
def dealJoinEvent(msgData):
    return '回复：regist申请，当前私人服务仅接受线下推荐。请通过朋友推荐给管理员后由管理员审核。'
def dealsetStrategyEvent(msgData):
    return '支持回测、监控策略。设置较为复杂，请手动访问web网站服务:otwind.cn(先别试了，网站还没空建呢)'
def dealstartMonitorEvent(msgData):
    #先用个比较搓的办法，写配置文件，userid ：1  后面再优化
    if writeCfg('monitor',msgData['FromUserName'],1):
        return '开始监控，请等待监控任务回复。'
def dealSetMonitorText(msgData):
    userid = msgData['FromUserName']
    content = msgData['Content']
    successCount = 0
    stockcodeMatch = re.findall('\d\d\d\d\d\d',content)
    strategyMatch = content.split('策略')[-1].split(',')
    if len(stockcodeMatch) == 0 :
        return False,'设置格式错误，未匹配到stock代码'
    if content.find('策略') == -1:
        return False,'设置格式错误，未匹配到策略关键字'
    strategyModel = getModel(tableName='wxcloudrun_strategyconfig',appLabel='wxcloudrun') 
    for stockcode in stockcodeMatch:
        #if stockcode.
        if not checkStockcodeValid(stockcode):
            logger.error('stockcode error,not in stockDB')
            continue
        for strategy in strategyMatch:
            if strategy not in strategyList:
                logger.error('startegy:'+strategy+' not in strategyList')
                continue
            strategyModel.objects.create(userid=userid,stockcode = stockcode,monitorStrategy=strategy,valid=False,validtime='',invalidtime='')
            successCount = successCount + 1
    queryUserStrategyList = strategyModel.objects.filter(userid=userid)
    return '设置成功:'+str(successCount)+'个,当前情况：'+str(queryUserStrategyList)
def dealSetMonitorEvent(msgData): 
    return '设置格式：监控000001,000002,策略1YC4X,fltp \r\n1、请严格按照格式配置。\r\n2、如果配置多个，则stock和策略为正交关系\r\n3、标点符号为英文格式 '  #后面换成URL交互设置
def dealClickEvent(msgData):
    if 'FromUserName' not in msgData.keys():  #只在第一层判断，后续函数默认正常
        logger.error('msg error, missing FromUserName!')
        return 'msg error, missing FromUserName!'
    if 'EventKey' not in msgData.keys():
        logger.error('msg error, missing EventKey!')
        return 'msg error, missing EventKey!'

    if msgData['EventKey'] == 'join':
        return dealJoinEvent(msgData)
    if  not checkUserValid(msgData['FromUserName']):  #除去join外，其他event不响应非法用户
        return '用户未注册或已禁用'
    if msgData['EventKey'] == 'setMonitor':
        return dealSetMonitorEvent(msgData)
    if msgData['EventKey'] == 'setStrategy':
        return dealsetStrategyEvent(msgData)
    if msgData['EventKey'] == 'startMonitor':
        return dealstartMonitorEvent(msgData)
    else:
        return '此功能暂未开放，项目延期中'

def dealRegistMsg(msgData):
    userid = msgData['FromUserName']
    curTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #userModel = get_model('wxcloudrun_usermanager',app_label='wxcloudrun')
    userModel = getModel(tableName='wxcloudrun_usermanager',appLabel='wxcloudrun')
    '''
    if 'wxcloudrun_usermanager' in modelsPoolDic.keys():
        userModel = modelsPoolDic['wxcloudrun_usermanager']
    else:
        userModel = getModel(tableName='wxcloudrun_usermanager',appLabel='wxcloudrun')
        modelsPoolDic['wxcloudrun_usermanager'] = userModel   #几千个表的model操作不知道要占用多少内存。
    '''
    queryUserList = userModel.objects.filter(userid=userid)
    
    if len(queryUserList) > 0:
        return '该用户已注册'
    userModel.objects.create(userid=userid,useraccount = '',username='',registtime=curTime,uuid='',level=0,valid=False,validtime='',cashflow=0)
    logger.info('try regist')
    #userModel.objects.bulk_create([userModel(userid=userid,user_account = '',username='',registtime=curTime,uuid='',level=0,valid=False,validtime='',cashflow=0)])
    try:
        user = userModel.objects.get(userid=userid)
    except:
        user = None
    if user != None and user.userid == userid:
        return '注册成功'
    else:
        return '注册失败，请联系管理员！'    
def dealTextMsg(msgData):
    if 'FromUserName' not in msgData.keys():  #只在第一层判断，后续函数默认正常
        logger.error('msg error, missing FromUserName!')
        return 'msg error, missing FromUserName!'
    if 'Content' not in msgData.keys():
        logger.error('msg error, missing Content!')
        return 'msg error, missing Content!'
    content = msgData['Content']
    if content.startswith('regist') and 'FromUserName' in msgData.keys():
        return dealRegistMsg(msgData)    
    if  not checkUserValid(msgData['FromUserName']):  #除去regist外，其他消息不处理
        return '用户未注册或已禁用'
    if content.startswith('m:'):
        res,message = dealSetMonitorText(msgData)
        if res:
            return '监控设置成功'
        else:
            return message

    return "default reply"