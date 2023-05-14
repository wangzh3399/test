# -*- coding: utf-8 -*-
# filename: menu.py
import requests
from basic import Basic

class Menu(object):
    def __init__(self):
        pass
    def create(self, postData, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % accessToken
        #if isinstance(postData, str):
            #postData = postData.encode('utf-8')
        resp = requests.post(postUrl, postData)
        print(resp.status_code)
        print(resp.text)

    def query(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token=%s" % accessToken
        resp = requests.post(url=postUrl)
        print(resp.status_code)
        print(resp.text)

    def delete(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s" % accessToken
        resp = requests.post(url=postUrl)
        print(resp.status_code)
        print(resp.text)
        
    #获取自定义菜单配置接口
    def get_current_selfmenu_info(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info?access_token=%s" % accessToken
        resp = requests.post(url=postUrl)
        print(resp.status_code)
        print(resp.text)

if __name__ == '__main__':
    myMenu = Menu()
    postJson = """
    {
        "button":
        [
            {
                "name": "未发布",
                "sub_button":
                [
                    {
                        "type": "click",
                        "name": "未发布",
                        "key": "defaultRecommend"
                    },
                    {
                        "type": "click",
                        "name": "未发布",
                        "key": "strategyRecommend"
                    },
                    {
                        "type": "click",
                        "name": "未发布",
                        "key": "chasingHotSpots"
                    }
                ]
            },
            {
                "name": "未发布",
                "sub_button":
                [
                    {
                        "type": "click",
                        "name": "未发布",
                        "key": "setMonitor"
                    },
                    {
                        "type": "click",
                        "name": "未发布",
                        "key": "startMonitor"
                    },
                    {
                        "type": "click",
                        "name": "未发布",
                        "key": "stopMonitor"
                    }
                ]
            },
            {
                "name": "未发布",
                "sub_button":
                [
                    {
                        "type": "click",
                        "name": "未发布",
                        "key": "join"
                    },
                    {
                        "type": "click",
                        "name": "未发布",
                        "key": "setStrategy"
                    },
                    {
                        "type": "view",
                        "name": "测试跳转URL",
                        "url":"http://wxservice.otwind.cn/wxui"
                    }
                ]
            }
          ]
    }
    """
    accessToken = Basic().get_access_token()
    #myMenu.delete(accessToken)
    myMenu.create(postJson.encode('utf-8'), accessToken)
    #myMenu.delete(accessToken)