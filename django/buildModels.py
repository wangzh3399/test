#encoding: utf-8
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wxcloudrun.settings") 
django.setup()

from django.apps import apps
import wxcloudrun.models as mdl
import traceback
from  basicfunc import *

modelsfile = 'wxcloudrun/models.py'
def getModelClassCentent(stockcode):
    stockModelContent = f'''
class stock_{stockcode}(models.Model):
    date = models.CharField(max_length=20,blank=False,primary_key=True,verbose_name="日期")
    open_cq = models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="除权开盘价")
    high_cq = models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="除权最高价")
    low_cq = models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="除权最低价")
    close_cq = models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="除权收盘价")
    open_hfq = models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="后复权开盘价")
    high_hfq = models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="后复权最高价")
    low_hfq = models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="后复权最低价")
    close_hfq = models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="后复权收盘价")
    volume = models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="成交量")
    turnover = models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="成交额")
    turnover_rate = models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="换手率")
    change_rate = models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="涨跌幅")
    amplitude = models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="振幅")
    pre_volume = models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="盘前成交量")
    pre_turnover = models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="盘前成交额")
    pre_turnover_rate = models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="盘前换手率")
    pre_change_rate = models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="盘前涨跌幅")
    after_volume = models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="盘后成交量")
    after_turnover = models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="盘后成交额")
    after_turnover_rate = models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="盘后换手率")
    after_change_rate = models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="盘后涨跌幅--应该没有意义，盘后固定价格交易")
    suspension = models.BooleanField(null=True,verbose_name="是否停牌。0否，1是")
    net_asset = models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="资产净值")
    net_profit = models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="净利润")
    earning_per_share = models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="每股盈利")
    outstanding_shares = models.IntegerField(blank=False,null=True,verbose_name="流通股本")
    net_asset_per_share = models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="每股净资产")
    circular_market_val = models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="流通市值")
    dma5_static = models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="静态5日均线")
    class Meta:
        db_table = 'stock_{stockcode}'
        app_label = 'wxcloudrun'
        verbose_name = 'stock_{stockcode}'
        verbose_name_plural = verbose_name

'''
    return stockModelContent
def buildModel():
    f = open(modelsfile,'a')
    stocks = mdl.stockbasicinfo.objects.all()
    for i in stocks:
        f.write(getModelClassCentent(i.stockcode))
    f.close()
if __name__ == "__main__":
    buildModel()