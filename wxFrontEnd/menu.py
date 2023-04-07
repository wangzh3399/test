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
                "name": "阅千帆",
                "sub_button":
                [
                    {
                        "type": "click",
                        "name": "锦囊妙计",
                        "key": "defaultRecommend"
                    },
                    {
                        "type": "click",
                        "name": "排沙简金",
                        "key": "strategyRecommend"
                    },
                    {
                        "type": "click",
                        "name": "洪水猛兽",
                        "key": "chasingHotSpots"
                    }
                ]
            },
            {
                "name": "观天象",
                "sub_button":
                [
                    {
                        "type": "click",
                        "name": "约法三章",
                        "key": "setMonitor"
                    },
                    {
                        "type": "click",
                        "name": "日出而作",
                        "key": "startMonitor"
                    },
                    {
                        "type": "click",
                        "name": "日落而息",
                        "key": "stopMonitor"
                    }
                ]
            },
            {
                "name": "理朝政",
                "sub_button":
                [
                    {
                        "type": "click",
                        "name": "良禽择木",
                        "key": "join"
                    },
                    {
                        "type": "click",
                        "name": "排兵布阵",
                        "key": "setStrategy"
                    },
                    {
                        "type": "click",
                        "name": "授业解惑",
                        "key": "help"
                    }
                ]
            }
          ]
    }
    """
    accessToken = Basic().get_access_token()
    #myMenu.delete(accessToken)
    myMenu.create(postJson.encode('utf-8'), accessToken)