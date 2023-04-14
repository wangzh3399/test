#在后台操作数据库的各类接口，不经过django的api接口，避免与用户接口产生较大的资源抢占。

import django
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib import admin
from django.db import models
import os
import re
from django.db import connection, migrations, models
from django.db.migrations.executor import MigrationExecutor
from django.apps import apps
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wxcloudrun.settings')
django.setup()
def getFields(tablename,datatype): #创建或查询时，根据表明返回field，dataype指定返回格式是list还是dic
    tablename = tablename.lower()
    datatype = datatype.lower()
    assert datatype=='list' or datatype=='dic'
    #数据库名都小写的
    assert tablename=='wxcloudrun_stockdata' or tablename=='wxcloudrun_stockstaticdata' or tablename=='wxcloudrun_strategyconfig' or tablename=='wxcloudrun_usermanager'
    stockDataFieldsList = [
        ('date' , models.CharField(max_length=20,blank=False,primary_key=True,verbose_name="日期")),
        ('open_cq' , models.DecimalField(max_digits=7,decimal_places=2,blank=False,null=True,verbose_name="除权开盘价")),
        ('high_cq' , models.DecimalField(max_digits=7,decimal_places=2,blank=False,null=True,verbose_name="除权最高价")),
        ('low_cq' , models.DecimalField(max_digits=7,decimal_places=2,blank=False,null=True,verbose_name="除权最低价")),
        ('close_cq' , models.DecimalField(max_digits=7,decimal_places=2,blank=False,null=True,verbose_name="除权收盘价")),
        ('open_hfq' , models.DecimalField(max_digits=9,decimal_places=2,blank=False,null=True,verbose_name="后复权开盘价")),
        ('high_hfq' , models.DecimalField(max_digits=9,decimal_places=2,blank=False,null=True,verbose_name="后复权最高价")),
        ('low_hfq' , models.DecimalField(max_digits=9,decimal_places=2,blank=False,null=True,verbose_name="后复权最低价")),
        ('close_hfq' , models.DecimalField(max_digits=9,decimal_places=2,blank=False,null=True,verbose_name="后复权收盘价")),
        ('dma5' , models.DecimalField(max_digits=7,decimal_places=2,blank=False,null=True,verbose_name="5日线")),
        ('dma10' , models.DecimalField(max_digits=7,decimal_places=2,blank=False,null=True,verbose_name="10日线")),
        ('dma20' , models.DecimalField(max_digits=7,decimal_places=2,blank=False,null=True,verbose_name="20日线")),
        ('dma30' , models.DecimalField(max_digits=7,decimal_places=2,blank=False,null=True,verbose_name="30日线")),
        ('wma5' , models.DecimalField(max_digits=7,decimal_places=2,blank=False,null=True,verbose_name="5周线")),
        ('wma10' , models.DecimalField(max_digits=7,decimal_places=2,blank=False,null=True,verbose_name="10周线")),
        ('wma20' , models.DecimalField(max_digits=7,decimal_places=2,blank=False,null=True,verbose_name="20周线")),
        ('wma30' , models.DecimalField(max_digits=7,decimal_places=2,blank=False,null=True,verbose_name="30周线")),
        ('mma5' , models.DecimalField(max_digits=7,decimal_places=2,blank=False,null=True,verbose_name="5月线")),
        ('mma10' , models.DecimalField(max_digits=7,decimal_places=2,blank=False,null=True,verbose_name="10月线")),
        ('mma20' , models.DecimalField(max_digits=7,decimal_places=2,blank=False,null=True,verbose_name="20月线")),
        ('mma30' , models.DecimalField(max_digits=7,decimal_places=2,blank=False,null=True,verbose_name="30月线")),
        ('volume' , models.DecimalField(max_digits=20,decimal_places=2,blank=False,null=True,verbose_name="成交量")),
        ('turnover' , models.DecimalField(max_digits=20,decimal_places=2,blank=False,null=True,verbose_name="成交额")),
        ('turnover_rate' , models.DecimalField(max_digits=7,decimal_places=6,blank=False,null=True,verbose_name="换手率")),
        ('change_rate' , models.DecimalField(max_digits=5,decimal_places=4,blank=False,null=True,verbose_name="涨跌幅")),
        ('amplitude' , models.DecimalField(max_digits=5,decimal_places=4,blank=False,null=True,verbose_name="振幅")),
        ('pre_volume' , models.DecimalField(max_digits=20,decimal_places=2,blank=False,null=True,verbose_name="盘前成交量")),
        ('pre_turnover' , models.DecimalField(max_digits=20,decimal_places=2,blank=False,null=True,verbose_name="盘前成交额")),
        ('pre_turnover_rate' , models.DecimalField(max_digits=7,decimal_places=6,blank=False,null=True,verbose_name="盘前换手率")),
        ('pre_change_rate' , models.DecimalField(max_digits=5,decimal_places=4,blank=False,null=True,verbose_name="盘前涨跌幅")),
        ('after_volume' , models.DecimalField(max_digits=20,decimal_places=2,blank=False,null=True,verbose_name="盘后成交量")),
        ('after_turnover' , models.DecimalField(max_digits=20,decimal_places=2,blank=False,null=True,verbose_name="盘后成交额")),
        ('after_turnover_rate' , models.DecimalField(max_digits=7,decimal_places=6,blank=False,null=True,verbose_name="盘后换手率")),
        ('after_change_rate' , models.DecimalField(max_digits=5,decimal_places=4,blank=False,null=True,verbose_name="盘后涨跌幅--应该没有意义，盘后固定价格交易")),
        ('suspension' , models.BooleanField(null=True,verbose_name="是否停牌。0否，1是")),
        ('net_asset' , models.DecimalField(max_digits=20,decimal_places=2,blank=False,null=True,verbose_name="资产净值")),
        ('net_profit' , models.DecimalField(max_digits=20,decimal_places=2,blank=False,null=True,verbose_name="净利润")),
        ('earning_per_share' , models.DecimalField(max_digits=5,decimal_places=2,blank=False,null=True,verbose_name="每股盈利")),
        ('outstanding_shares' , models.IntegerField(blank=False,null=True,verbose_name="流通股本")),
        ('net_asset_per_share' , models.DecimalField(max_digits=5,decimal_places=2,blank=False,null=True,verbose_name="每股净资产")),
        ('circular_market_val' , models.DecimalField(max_digits=20,decimal_places=2,blank=False,null=True,verbose_name="流通市值")),
        ('data_check_flag' , models.CharField(max_length=20,blank=False,verbose_name="数据校验标志")),
        ('data_last_check_date' , models.CharField(max_length=20,blank=False,verbose_name="最后一次校验时间")),
        ('data_check_by_userid' , models.CharField(max_length=20,blank=False,verbose_name="负责校验的用户id"))
    ]
    stockDataFieldsDic = {
        'date' : models.CharField(max_length=20,blank=False,primary_key=True,verbose_name="日期"),
        'open_cq' : models.DecimalField(max_digits=7,decimal_places=2,blank=False,null=True,verbose_name="除权开盘价"),
        'high_cq' : models.DecimalField(max_digits=7,decimal_places=2,blank=False,null=True,verbose_name="除权最高价"),
        'low_cq' : models.DecimalField(max_digits=7,decimal_places=2,blank=False,null=True,verbose_name="除权最低价"),
        'close_cq' : models.DecimalField(max_digits=7,decimal_places=2,blank=False,null=True,verbose_name="除权收盘价"),
        'open_hfq' : models.DecimalField(max_digits=9,decimal_places=2,blank=False,null=True,verbose_name="后复权开盘价"),
        'high_hfq' : models.DecimalField(max_digits=9,decimal_places=2,blank=False,null=True,verbose_name="后复权最高价"),
        'low_hfq' : models.DecimalField(max_digits=9,decimal_places=2,blank=False,null=True,verbose_name="后复权最低价"),
        'close_hfq' : models.DecimalField(max_digits=9,decimal_places=2,blank=False,null=True,verbose_name="后复权收盘价"),
        'volume' : models.DecimalField(max_digits=20,decimal_places=2,blank=False,null=True,verbose_name="成交量"),
        'turnover' : models.DecimalField(max_digits=20,decimal_places=2,blank=False,null=True,verbose_name="成交额"),
        'turnover_rate' : models.DecimalField(max_digits=7,decimal_places=6,blank=False,null=True,verbose_name="换手率"),
        'change_rate' : models.DecimalField(max_digits=5,decimal_places=4,blank=False,null=True,verbose_name="涨跌幅"),
        'amplitude' : models.DecimalField(max_digits=5,decimal_places=4,blank=False,null=True,verbose_name="振幅"),
        'pre_volume' : models.DecimalField(max_digits=20,decimal_places=2,blank=False,null=True,verbose_name="盘前成交量"),
        'pre_turnover' : models.DecimalField(max_digits=20,decimal_places=2,blank=False,null=True,verbose_name="盘前成交额"),
        'pre_turnover_rate' : models.DecimalField(max_digits=7,decimal_places=6,blank=False,null=True,verbose_name="盘前换手率"),
        'pre_change_rate' : models.DecimalField(max_digits=5,decimal_places=4,blank=False,null=True,verbose_name="盘前涨跌幅"),
        'after_volume' : models.DecimalField(max_digits=20,decimal_places=2,blank=False,null=True,verbose_name="盘后成交量"),
        'after_turnover' : models.DecimalField(max_digits=20,decimal_places=2,blank=False,null=True,verbose_name="盘后成交额"),
        'after_turnover_rate' : models.DecimalField(max_digits=7,decimal_places=6,blank=False,null=True,verbose_name="盘后换手率"),
        'after_change_rate' : models.DecimalField(max_digits=5,decimal_places=4,blank=False,null=True,verbose_name="盘后涨跌幅--应该没有意义，盘后固定价格交易"),
        'suspension' : models.BooleanField(null=True,verbose_name="是否停牌。0否，1是"),
        'net_asset' : models.DecimalField(max_digits=20,decimal_places=2,blank=False,null=True,verbose_name="资产净值"),
        'net_profit' : models.DecimalField(max_digits=20,decimal_places=2,blank=False,null=True,verbose_name="净利润"),
        'earning_per_share' : models.DecimalField(max_digits=5,decimal_places=2,blank=False,null=True,verbose_name="每股盈利"),
        'outstanding_shares' : models.IntegerField(blank=False,null=True,verbose_name="流通股本"),
        'net_asset_per_share' : models.DecimalField(max_digits=5,decimal_places=2,blank=False,null=True,verbose_name="每股净资产"),
        'circular_market_val' : models.DecimalField(max_digits=20,decimal_places=2,blank=False,null=True,verbose_name="流通市值"),
        'data_check_flag' : models.CharField(max_length=20,blank=False,verbose_name="数据校验标志"),
        'data_last_check_date' : models.CharField(max_length=20,blank=False,verbose_name="最后一次校验时间"),
        'data_check_by_userid' : models.CharField(max_length=20,blank=False,verbose_name="负责校验的用户id")
    }

    #后面改一下，分基础数据表和全量数据表
    stockStaticDataFieldsList = [
        ('stockcode' , models.CharField(max_length=8,blank=False,primary_key=True,verbose_name="股票id")),
        ('stockname' , models.CharField(max_length=32,blank=False,verbose_name="股票名称"))
    ]
    stockStaticDataFieldsDic = {
        'stockcode' : models.CharField(max_length=8,blank=False,primary_key=True,verbose_name="股票id"),
        'stockname' : models.CharField(max_length=32,blank=False,verbose_name="股票名称")
    }
    #每次重新激活策略要重新创建一条记录。
    strategyConfigFieldsList = [
        ('userid' , models.CharField(max_length=32,blank=False,primary_key=True,verbose_name="用户id")),
        ('stockcode' , models.CharField(max_length=8,blank=False,verbose_name="股票id")),
        ('monitorstrategy' , models.CharField(max_length=8,blank=False,verbose_name="监控策略")),   #这里区分快策略和慢策略。
        ('valid' , models.BooleanField(null=True,verbose_name="生效状态")),
        ('validtime' , models.CharField(max_length=20,blank=False,verbose_name="截止有效时间")),
        ('invalidtime' , models.CharField(max_length=20,blank=False,verbose_name="失效时间"))
        ]
    strategyConfigFieldsDic = {
        'userid' : models.CharField(max_length=32,blank=False,primary_key=True,verbose_name="用户id"),
        'stockcode' : models.CharField(max_length=8,blank=False,verbose_name="股票id"),
        'monitorstrategy' : models.CharField(max_length=8,blank=False,verbose_name="监控策略"),   #这里区分快策略和慢策略。
        'valid' : models.BooleanField(null=True,verbose_name="生效状态"),
        'validtime' : models.CharField(max_length=20,blank=False,verbose_name="截止有效时间"),
        'invalidtime' : models.CharField(max_length=20,blank=False,verbose_name="失效时间")
    }

    usermanagerFieldsList = [
        ('userid' , models.CharField(max_length=32,blank=False,primary_key=True,verbose_name="用户id")),
        ('useraccount' , models.CharField(max_length=32,blank=False,verbose_name="微信的账号用户名")),
        ('username' , models.CharField(max_length=32,blank=False,verbose_name="微信昵称")), 
        ('registtime' , models.CharField(max_length=20,blank=False,verbose_name="注册时间")),
        ('uuid' , models.CharField(max_length=32,blank=False,verbose_name="用户标识")),   #忘记要干嘛用的了
        ('level' , models.CharField(max_length=8,blank=False,verbose_name="用户等级")),  #level 999 管理员 
        ('valid' , models.BooleanField(null=True,verbose_name="生效状态")),
        ('validtime' , models.CharField(max_length=20,blank=False,verbose_name="截止有效时间")),
        ('cashflow' , models.IntegerField(blank=False,null=True,verbose_name="流水"))
        ]  

    usermanagerFieldsDic = {
        'userid' : models.CharField(max_length=32,blank=False,primary_key=True,verbose_name="用户id"),
        'useraccount' : models.CharField(max_length=32,blank=False,verbose_name="微信的账号用户名"),
        'username' : models.CharField(max_length=32,blank=False,verbose_name="微信昵称"), 
        'registtime' : models.CharField(max_length=20,blank=False,verbose_name="注册时间"),
        'uuid' : models.CharField(max_length=32,blank=False,verbose_name="用户标识"),   #忘记要干嘛用的了
        'level' : models.CharField(max_length=8,blank=False,verbose_name="用户等级"),  #level 999 管理员 
        'valid' : models.BooleanField(null=True,verbose_name="生效状态"),
        'validtime' : models.CharField(max_length=20,blank=False,verbose_name="截止有效时间"),
        'cashflow' : models.IntegerField(blank=False,null=True,verbose_name="流水") 
        }
    listMap = {
        'wxcloudrun_stockdata':stockDataFieldsList,
        'wxcloudrun_stockstaticdata':stockStaticDataFieldsList,
        'wxcloudrun_strategyconfig':strategyConfigFieldsList,
        'wxcloudrun_usermanager':usermanagerFieldsList
    }
    dicMap = {
        'wxcloudrun_stockdata':stockDataFieldsDic,
        'wxcloudrun_stockstaticdata':stockStaticDataFieldsDic,
        'wxcloudrun_strategyconfig':strategyConfigFieldsDic,
        'wxcloudrun_usermanager':usermanagerFieldsDic
    }
    if datatype == 'list':
        return listMap[tablename]
    else:
        return dicMap[tablename]
#维护一个大表，以自增ID为key，插入股票除权信息,暂时不搞了
'''
stockCQinfoFields = [
    ('id' , models.CharField(max_length=20,blank=False,primary_key=True,verbose_name="日期")),  
    ('stockcode' , models.CharField(max_length=20,blank=False,primary_key=True,verbose_name="日期")),
    ('stockCQFlag' , models.CharField(max_length=20,blank=False,primary_key=True,verbose_name="日期")),   #使用二进制进行位运算。标记是否分红、送转等等。
    ('stockCQDetail' , models.CharField(max_length=20,blank=False,primary_key=True,verbose_name="日期")),   #需要定义除权的类别格式等
    ('data_check_flag' , models.CharField(max_length=20,blank=False,primary_key=True,verbose_name="上市时间")),
    ('data_last_check_date' , models.CharField(max_length=20,blank=False,primary_key=True,verbose_name="上市时间")),
    ('data_check_by_userid' , models.CharField(max_length=20,blank=False,primary_key=True,verbose_name="上市时间"))
]
'''


def doMigrate(table_name, app_label, model_fields = None):
    class Migration(migrations.Migration):
        #initial = True
        #dependencies = []
        operations = [
            migrations.CreateModel(
                name=table_name,
                fields=model_fields,
            )
        ]

    executor = MigrationExecutor(connection)
    migration = Migration(table_name, app_label)
    with connection.schema_editor(atomic=True) as schema_editor:
        migration.apply(executor._create_project_state(), schema_editor)
 
def create_table(tableName,applabel):  #这里的tablename不带前缀applabel,或者传入stockcode
    if len(re.findall('\d\d\d\d\d\d',tableName)) != 0:
        doMigrate('stockdata_'+tableName,applabel,getFields('stockdata','list'))
        return
    #这里最好判断下是否创建成功。这里不能调用getModel判断，否则外层调用getModel，会死循环。
    doMigrate(tableName,applabel,getFields(tableName,'list'))
    #doMigrate('stockstaticdata','wxcloudrun',getFields('stockstaticdata','list'))
    #doMigrate('strategyconfig','wxcloudrun',getFields('strategyconfig','list'))
    #doMigrate('usermanager','wxcloudrun',getFields('usermanager','list'))
    #doMigrate('stockData',stockCQinfoFields)


def create_model(name, fields=None, app_label='', module='', options=None, admin=None):
    class Meta:
        pass
    if app_label:
        setattr(Meta, 'app_label', app_label)
    if options is not None:
        for key, value in options.items():
            setattr(Meta, key, value)
    attrs = {'__module__': module, 'Meta': Meta}
    if fields:
        attrs.update(fields)
    # 继承models.Model
    return type(name, (models.Model,), attrs)


def getModel(tableName,appLabel):
    #getModel如果还抛出异常，可能是表没创建？需要验证下，或者下面也可以建表
    """
    动态创建数据模型
    :param tableName: 表名
    :param appLabel: wxcloudrun  这字段没啥卵用？
    :return: 返回模型类
    """
    options = {'ordering': [], 'db_table': tableName, }
    try:
        #如果存在已注册的model，则不需要了。
        custom_model = apps.get_model(app_label = appLabel,model_name = tableName)
    except:
        custom_model = create_model(tableName, getFields(tableName,'dic'), options=options, app_label=appLabel, module='wxcloudrun.models')
    return custom_model

def tests(requests):
    # custom_model = create_table('example', fields,
    #                              app_label='app',
    #                           )
    afields = dict(title=models.CharField(choices=[('MR', 'Mr.'),
                                                   ('MRS', 'Mrs.'),
                                                   ('MS', 'Ms.')], max_length=3),
                   birth_date=models.DateField(blank=True, null=True)
                   )
 
    a_m = get_model('app01_a', app_label='app01', fields=afields)  # 参数1和法1不同
 
    bfields = dict(
        name=models.CharField(max_length=100),
        authors=a_m   # 这里和法1不同
    )
    model = get_model('app01_b', app_label='app01', fields=bfields)  # 参数1和法1不同
 
    # a_obj = obj.objects.get(id=1)
    print(model.objects.values('name'))
    obj = model.objects.filter(id=1).first()
    # a = obj
    a = obj.authors.objects.all()  # 参数1和法1不同
    print(a)
 