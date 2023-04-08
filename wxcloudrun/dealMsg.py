import wechatpy
from basicfunc import *
import traceback
import datetime
import sys


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



def dealJoinEvent(msgData):
    return '回复：regist申请，当前私人服务仅接受线下推荐。请通过朋友推荐给管理员后由管理员审核。'
def dealsetStrategyEvent(msgData):
    return '支持回测、监控策略。设置较为复杂，请手动访问web网站服务:otwind.cn'

def dealSetMonitorEvent(msgData): #这里应该是可以通过modle去访问数据库，先暂时使用db cursor
    dbconn  = getDBConn()
    dbCursor = dbconn.cursor()
    if 'FromUserName' not in msgData.keys():
        logger.error('msg error, missing FromUserName!')
        return 'msg error, missing FromUserName!'
    userid =  msgData['FromUserName']
    try:
        selectCmd = 'select count(*) from wxcloudrun_usermanager where userid="'+userid+'" and valid=True;'
        dbCursor.execute(selectCmd)
        selectRes = dbCursor.fetchone()
    except:
        logger.error('db error!\r\n'+traceback.format_exc())
        dbconn.close()
        return 'db error!\r\n'+traceback.format_exc()
    dbconn.close()  
    if selectRes == None:
        logger.info('db error,user match null!')
        return 'db error,user match null!'
    if int(selectRes[0]) == 0:
        logger.info('未授权用户，请授权后重试')
        return '未授权用户，请授权后重试'
    return '设置格式：m:000001,s:001'  #后面换成URL交互设置
def dealClickEvent(msgData):
    if 'EventKey' not in msgData.keys():
        logger.error('msg error, missing EventKey!')
        return 'msg error, missing EventKey!'
    if msgData['EventKey'] == 'Join':
        return dealJoinEvent(msgData)
    if msgData['EventKey'] == 'setMonitor':
        return dealSetMonitorEvent(msgData)
    if msgData['EventKey'] == 'setStrategy':
        return dealsetStrategyEvent(msgData)
    else:
        return '此功能暂未开放，项目延期中'

def dealRegistMsg(msgData):
    userid = msgData['FromUserName']
    curTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    selectCmd = 'select userid,registtime from wxcloudrun_usermanager where userid="'+userid+'";'
    insertCmd = 'insert into wxcloudrun_usermanager (userid,user_account,username,registtime,uuid,level,valid,validtime，cashflow) VALUE ("'+\
        userid +'","","",'+curTime+'"",0,'+False+',"","");'
    try:
        dbconn  = getDBConn()
        dbCursor = dbconn.cursor()
        dbCursor.execute(selectCmd)
        selectRes = dbCursor.fetchone()
        if selectRes == None:
            #新用户，注册
            dbCursor.execute(insertCmd)
            dbCursor.execute(selectCmd)
            selectRes = dbCursor.fetchone()
            if selectRes == None:
                logger.error('regist fail!')
                return '注册失败，请联系管理员'
            else:
                return '注册成功，用户id:'+selectRes[0]+',注册时间:'+selectRes[1]
        else:
            dbconn.close()
            return '该用户已注册'
    except:
        dbconn.close()
        logger.error('db error!\r\n'+traceback.format_exc())
        return 'db error!\r\n'+traceback.format_exc()
    
    return '注册成功'    
def dealTextMsg(msgData):
    if 'Content' not in msgData.keys():
        logger.error('msg error, missing Content!')
        return 'msg error, missing Content!'
    content = msgData['msgData']
    if content.startswith('m:'):
        return '监控设置成功'
    if content.startswith('regist') and 'FromUserName' in msgData.keys():
         return dealRegistMsg(msgData)