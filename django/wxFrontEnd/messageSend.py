# -*- coding: utf-8 -*-
# filename: menu.py
import requests
from basic import Basic
#import wechatpy
import json
accessToken = Basic().get_access_token()
def addKfAccount(account,nickname,password,accessToken):
    postUrl = "https://api.weixin.qq.com/customservice/kfaccount/add?access_token=%s" % accessToken

    postDic = {
     "kf_account" : account,
     "nickname" : nickname,
     "password" : password
}
    postData = json.dumps(postDic, indent=4)

    resp = requests.post(postUrl,postData)
    print(resp.status_code)
    print(resp.text)
def sendmsg(userid,msg):
    postUrl = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s" % accessToken

    postDic = {
    "touser":userid,
    "msgtype":"text",
    "text":
    {
         "content":msg
    }
}
    postData = json.dumps(postDic, indent=4,ensure_ascii=False).encode('utf-8')

    resp = requests.post(postUrl,postData)
    print(resp.status_code)
    print(resp.text)
def queryKfAccount(accessToken):
    postUrl = "https://api.weixin.qq.com/cgi-bin/customservice/getkflist?access_token=%s" % accessToken

    resp = requests.post(postUrl)
    print(resp.status_code)
    print(resp.text)

if __name__ == '__main__':
    userid = 'oHqS86cHPMo7D0_2xb8pd6VranAU'
    msg = '想吃鱼了'
    sendmsg(userid,msg) 
    #queryKfAccount(accessToken)
    #addKfAccount('wxid_8fy315k6072212@PrivateService','eee','FUCKfuck123',accessToken)