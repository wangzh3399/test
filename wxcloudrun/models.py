from datetime import datetime

from django.db import models


# Create your models here.
class stockData(models.Model):  #这个作为表模板，后面股票信息使用这个表动态快速批量建表
    date = models.CharField(max_length=20,blank=False,primary_key=True,verbose_name="日期")
    open_cq = models.DecimalField(max_digits=7,decimal_places=2,blank=False,null=True,verbose_name="除权开盘价")
    high_cq = models.DecimalField(max_digits=7,decimal_places=2,blank=False,null=True,verbose_name="除权最高价")
    low_cq = models.DecimalField(max_digits=7,decimal_places=2,blank=False,null=True,verbose_name="除权最低价")
    close_cq = models.DecimalField(max_digits=7,decimal_places=2,blank=False,null=True,verbose_name="除权收盘价")
    open_hfq = models.DecimalField(max_digits=9,decimal_places=2,blank=False,null=True,verbose_name="后复权开盘价")
    high_hfq = models.DecimalField(max_digits=9,decimal_places=2,blank=False,null=True,verbose_name="后复权最高价")
    low_hfq = models.DecimalField(max_digits=9,decimal_places=2,blank=False,null=True,verbose_name="后复权最低价")
    close_hfq = models.DecimalField(max_digits=9,decimal_places=2,blank=False,null=True,verbose_name="后复权收盘价")
    volume = models.DecimalField(max_digits=20,decimal_places=2,blank=False,null=True,verbose_name="成交量")
    turnover = models.DecimalField(max_digits=20,decimal_places=2,blank=False,null=True,verbose_name="成交额")
    turnover_rate = models.DecimalField(max_digits=7,decimal_places=6,blank=False,null=True,verbose_name="换手率")
    change_rate = models.DecimalField(max_digits=5,decimal_places=4,blank=False,null=True,verbose_name="涨跌幅")
    amplitude = models.DecimalField(max_digits=5,decimal_places=4,blank=False,null=True,verbose_name="振幅")
    pre_volume = models.DecimalField(max_digits=20,decimal_places=2,blank=False,null=True,verbose_name="盘前成交量")
    pre_turnover = models.DecimalField(max_digits=20,decimal_places=2,blank=False,null=True,verbose_name="盘前成交额")
    pre_turnover_rate = models.DecimalField(max_digits=7,decimal_places=6,blank=False,null=True,verbose_name="盘前换手率")
    pre_change_rate = models.DecimalField(max_digits=5,decimal_places=4,blank=False,null=True,verbose_name="盘前涨跌幅")
    after_volume = models.DecimalField(max_digits=20,decimal_places=2,blank=False,null=True,verbose_name="盘后成交量")
    after_turnover = models.DecimalField(max_digits=20,decimal_places=2,blank=False,null=True,verbose_name="盘后成交额")
    after_turnover_rate = models.DecimalField(max_digits=7,decimal_places=6,blank=False,null=True,verbose_name="盘后换手率")
    after_change_rate = models.DecimalField(max_digits=5,decimal_places=4,blank=False,null=True,verbose_name="盘后涨跌幅--应该没有意义，盘后固定价格交易")
    suspension = models.BooleanField(null=True,verbose_name="是否停牌。0否，1是")
    net_asset = models.DecimalField(max_digits=20,decimal_places=2,blank=False,null=True,verbose_name="资产净值")
    net_profit = models.DecimalField(max_digits=20,decimal_places=2,blank=False,null=True,verbose_name="净利润")
    earning_per_share = models.DecimalField(max_digits=5,decimal_places=2,blank=False,null=True,verbose_name="每股盈利")
    outstanding_shares = models.IntegerField(blank=False,null=True,verbose_name="流通股本")
    net_asset_per_share = models.DecimalField(max_digits=5,decimal_places=2,blank=False,null=True,verbose_name="每股净资产")
    circular_market_val = models.DecimalField(max_digits=20,decimal_places=2,blank=False,null=True,verbose_name="流通市值")
    data_check_flag = models.CharField(max_length=20,blank=False,primary_key=True,verbose_name="上市时间")
    data_last_check_date = models.CharField(max_length=20,blank=False,primary_key=True,verbose_name="上市时间")
    data_check_by_userid = models.CharField(max_length=20,blank=False,primary_key=True,verbose_name="上市时间")

class stockStaticData(models.Model):  #后面改一下，分基础数据表和全量数据表
    stockcode = models.CharField(max_length=8,blank=False,primary_key=True,verbose_name="股票id")
    stockName = models.CharField(max_length=32,blank=False,primary_key=True,verbose_name="股票id")

class strategyConfig(models.Model):  #每次重新激活策略要重新创建一条记录。
    stockname = models.CharField(max_length=32,blank=False,primary_key=True,verbose_name="用户id")
    stockcode = models.CharField(max_length=8,blank=False,primary_key=True,verbose_name="股票id")
    monitorscheme = models.CharField(max_length=8,blank=False,primary_key=True,verbose_name="监控策略")   #这里区分快策略和慢策略。
    valid = models.BooleanField(null=True,verbose_name="生效状态")
    validtime = models.CharField(max_length=20,blank=False,primary_key=True,verbose_name="截止有效时间")
    invalidtime = models.CharField(max_length=20,blank=False,primary_key=True,verbose_name="失效时间")


class usermanager(models.Model):  #
    userid = models.CharField(max_length=32,blank=False,primary_key=True,verbose_name="用户id")
    user_account = models.CharField(max_length=32,blank=False,primary_key=True,verbose_name="微信的账号用户名")
    username = models.CharField(max_length=32,blank=False,primary_key=True,verbose_name="微信昵称")  
    registtime = models.CharField(max_length=20,blank=False,primary_key=True,verbose_name="注册时间")
    uuid = models.CharField(max_length=32,blank=False,primary_key=True,verbose_name="用户标识")
    level = models.CharField(max_length=8,blank=False,primary_key=True,verbose_name="用户等级")
    valid = models.BooleanField(null=True,verbose_name="生效状态")
    validtime = models.CharField(max_length=20,blank=False,primary_key=True,verbose_name="截止有效时间")
    cashflow = models.IntegerField(blank=False,null=True,verbose_name="流水")


class stockCQinfo(models.Model):  #维护一个大表，以自增ID为key，插入股票除权信息。
    id = models.CharField(max_length=20,blank=False,primary_key=True,verbose_name="日期")  
    stockcode = models.CharField(max_length=20,blank=False,primary_key=True,verbose_name="日期")
    stockCQFlag = models.CharField(max_length=20,blank=False,primary_key=True,verbose_name="日期")   #使用二进制进行位运算。标记是否分红、送转等等。
    stockCQDetail = models.CharField(max_length=20,blank=False,primary_key=True,verbose_name="日期")   #需要定义除权的类别格式等
    data_check_flag = models.CharField(max_length=20,blank=False,primary_key=True,verbose_name="上市时间")
    data_last_check_date = models.CharField(max_length=20,blank=False,primary_key=True,verbose_name="上市时间")
    data_check_by_userid = models.CharField(max_length=20,blank=False,primary_key=True,verbose_name="上市时间")
