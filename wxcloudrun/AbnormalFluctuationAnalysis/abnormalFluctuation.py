import requests
import urllib3
import time



class stock():
    def __init__(self):
        stock = {}
    



def spiderSSEAnnouncements(startDate=1,endDate=1,bulletinType=13):
    #官网有交易条件过滤，可以先实现异常波动的，后面再封装。
    healder = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Referer': 'http://www.sse.com.cn/',
        'Cookie': 'ba17301551dcbaf9_gdp_user_key=;ba17301551dcbaf9_gdp_session_id=89c962bb-1b82-44b6-a62b-d7ae62db381c;gdp_user_id=gioenc-8agg5dg5%2C4d2g%2C590g%2C9dd6%2C8eg41g64gb73;ba17301551dcbaf9_gdp_session_id_89c962bb-1b82-44b6-a62b-d7ae62db381c=true;ba17301551dcbaf9_gdp_sequence_ids={%22globalKey%22:7%2C%22VISIT%22:2%2C%22PAGE%22:2%2C%22VIEW_CLICK%22:4%2C%22CUSTOM%22:2}'



    }
    http = urllib3.PoolManager(num_pools=5, headers=healder)
    #s = requests.Session()
    url = 'http://query.sse.com.cn/security/stock/queryCompanyBulletinNew.do?\
        jsonCallBack=jsonpCallback36508105\
        &isPagination=true\
        &pageHelp.pageSize=25\
        &pageHelp.cacheSize=1\
        &START_DATE=2022-12-27\
        &END_DATE=2023-03-27\
        &SECURITY_CODE=\
        &TITLE=\
        &BULLETIN_TYPE=13\
        &stockType=\
        &pageHelp.pageNo=1\
        &pageHelp.beginPage=1\
        &pageHelp.endPage=1\
        &_=1679836706420'.replace(' ','')
    #r1 = s.get(url)
    resp = http.request('GET',url,body='')
    print(resp.data)
    pass


def spiderSZSEAnnouncements():
    pass


if __name__ == '__main__':
    
    spiderSSEAnnouncements()