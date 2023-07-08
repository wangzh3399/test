from basicfunc import *
import akshare as ak
import traceback
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wxcloudrun.settings") 
django.setup()
from django.db.models import *
import wxcloudrun.models as mdl


def fullUpdateLocal(stockModel):
    #从基础的txt更新一次，后面再定期扫描。 这里还有个问题，股票名称还没有获取到，先使用id吧，后面再加
    stocklist = open('./stocklist.txt','r')
    for stockcode in stocklist:
        stockModel.objects.create(stockcode = stockcode,stockname = '')
def UpdateOnline(stockModel): #全量更新基本上30s以内
    stockinfoDf = ak.stock_info_a_code_name()
    #stockinfoDf_sz = ak.stock_info_sz_name_code()
    print(stockinfoDf)
    '''
        code   name                                                                                                                                                                                                                                             
0     000001   平安银行
1     000002  万  科Ａ
2     000004   ST国华
3     000005   ST星源
4     000006   深振业Ａ
...      ...    ...
5129  873169   七丰精工
5130  873223   荣亿精密
5131  873305   九菱科技
5132  873339   恒太照明
5133  873527    夜光明
    '''  
    for i in range(0,len(stockinfoDf.index)):
        stockModel.objects.get_or_create(stockcode = stockinfoDf['code'][i],stockname = stockinfoDf['name'][i])

if __name__ == '__main__':
    UpdateOnline(mdl.stockbasicinfo)