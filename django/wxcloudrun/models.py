from datetime import datetime

from django.db import models
from django.apps import apps
from django.core.management import call_command 

# Create your models here.
class stockbasicinfo(models.Model): #股票基础信息，一个表存所有stock的信息
    stockcode=models.CharField(max_length=8,blank=False,primary_key=True,verbose_name="股票id")
    stockname=models.CharField(max_length=32,blank=False,verbose_name="股票名称")
    class Meta:
        # 设置表名
        db_table = "stockbasicinfo"
        verbose_name = "股票基础信息"  
        verbose_name_plural = verbose_name  #这个选项是指定，模型的复数形式
        abstract = False    #定义当前的模型是不是一个抽象类,抽象类不建数据库表，用于继承。
class usermanager(models.Model): #model的meta有
    userid = models.CharField(max_length=32,blank=False,primary_key=True,verbose_name="用户id")  #这里用户id实际长度 28，如：oHqS86cHPMo7D0_2xb8pd6VranAU
    useraccount = models.CharField(max_length=32,blank=True,verbose_name="微信的账号用户名")
    username = models.CharField(max_length=32,blank=True,verbose_name="微信昵称")
    registtime = models.CharField(max_length=20,blank=True,verbose_name="注册时间")
    uuid = models.CharField(max_length=32,blank=True,verbose_name="用户标识")
    level = models.CharField(max_length=8,blank=True,verbose_name="用户等级")  #level 999 管理员 
    valid = models.BooleanField(blank=True,verbose_name="生效状态")
    validtime = models.CharField(max_length=20,blank=True,verbose_name="截止有效时间")
    cashflow = models.IntegerField(blank=True,verbose_name="流水")
    class Meta:
        # 设置表名
        db_table = "usermanager"
        verbose_name = "用户管理"  
        verbose_name_plural = verbose_name  #这个选项是指定，模型的复数形式
        abstract = False    #定义当前的模型是不是一个抽象类,抽象类不建数据库表，用于继承。    
class conditions(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256,blank=True,verbose_name="条件名")
    funcname = models.CharField(max_length=256,blank=True,verbose_name="条件函数名")
    desc = models.CharField(max_length=256,blank=True,verbose_name="条件描述")
    condtype = models.CharField(max_length=16,blank=True,verbose_name="类型")  #暂时没考虑好，可能后面可以用于可交易的或私有的。
    argvsnum = models.IntegerField(blank=True,null=True,verbose_name="参数个数")
    argvsdesc = models.CharField(max_length=256,blank=True,verbose_name="参数描述") #[持续天数(限定条件说明),用于比较的固定值,xxxx]
    retvalnum = models.IntegerField(blank=True,null=True,verbose_name="返回值个数")
    retvaldesc = models.CharField(max_length=256,blank=True,verbose_name="参数描述") #[持续天数(限定条件说明),用于比较的固定值,xxxx]
    creatorid = models.CharField(max_length=32,blank=True,verbose_name="用户id")
    createtime = models.CharField(max_length=20,blank=True,verbose_name="创建时间")
    changetime = models.DateTimeField(auto_now = True,verbose_name="变更时间")
    class Meta:
        # 设置表名
        db_table = "conditonpool"
        verbose_name = "条件表"  
        verbose_name_plural = verbose_name  #这个选项是指定，模型的复数形式
        abstract = False    #定义当前的模型是不是一个抽象类,抽象类不建数据库表，用于继承。 
class strategys(models.Model): 
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=16,blank=True,verbose_name="策略名") #策略名
    desc = models.CharField(max_length=256,blank=True,verbose_name="策略描述")
    sttype = models.CharField(max_length=16,blank=True,verbose_name="策略类型")   #暂时没考虑好，可能后面可以用于可交易的或私有的。
    expression = models.CharField(max_length=256,blank=True,verbose_name="策略表达式") 
    ownderid = models.CharField(max_length=32,blank=True,verbose_name="拥有者id") #外键，CASCADE关联删除   PROTECT保护处理  SET_NULL置空处理  DO_NOTHING不处理
    creatorid = models.CharField(max_length=32,blank=True,verbose_name="创建者id")   #随着策略交易，可能某些策略会属于不同的人。  通过策略拥有者和创建者一致性判断是否是购买的策略
    createtime = models.CharField(max_length=20,blank=True,verbose_name="创建时间")
    owntime = models.CharField(max_length=20,blank=True,verbose_name="归属时间")  #策略归属于拥有者的时间
    changetime = models.DateTimeField(auto_now = True,verbose_name="变更时间") #策略被修改时间，可以是创建者或者拥有者
    validtime = models.CharField(max_length=20,blank=True,verbose_name="有效期") #策略可以以使用时间作为交易。
    runstatus = models.CharField(max_length=16,blank=True,verbose_name="策略运行状态")  #创建状态、回测状态、发布状态、下架状态、生效中等
    buyoutprice = models.IntegerField(blank=True,null=True,verbose_name="买断售价")  #买断：购买者可明文查看策略内容、编辑扩展等。
    unitprice = models.IntegerField(blank=True,null=True,verbose_name="购买时间单价")  #时间单价以交易日按天计算 
    protectlevel = models.IntegerField(blank=True,null=True,verbose_name="策略保护级别")  #购买者在买断后
    linkid = models.IntegerField(blank=True,null=True,verbose_name="绑定到某个策略") #当策略有linkid时，处于维护状态，以link过去的策略id作为实际策略。
    popular = models.IntegerField(blank=True,null=True,verbose_name="策略点赞热度")  #用户点赞热度。
    class Meta:
        # 设置表名
        db_table = "strategypool"
        verbose_name = "用户策略"  
        verbose_name_plural = verbose_name  #这个选项是指定，模型的复数形式
        abstract = False    #定义当前的模型是不是一个抽象类,抽象类不建数据库表，用于继承。

class stockpool(models.Model):#股票池表，用户可以自定义股票池，用于应用不同策略
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=16,blank=True,verbose_name="股票池名称") #策略名
    desc = models.CharField(max_length=256,blank=True,verbose_name="股票池描述")
    stockpooltype = models.CharField(max_length=16,blank=True,verbose_name="股票池类型") 
    creatorid = models.CharField(max_length=32,blank=True,verbose_name="所属用户id")
    createtime = models.CharField(max_length=20,blank=True,verbose_name="创建时间")
    changetime = models.DateTimeField(auto_now = True,verbose_name="变更时间")
    class Meta:
        # 设置表名
        db_table = "stockpool"
        verbose_name = "股票池"  
        verbose_name_plural = verbose_name  #这个选项是指定，模型的复数形式
        abstract = False    #定义当前的模型是不是一个抽象类,抽象类不建数据库表，用于继承。
class monitortask(models.Model): #r任务绑定某一个股票池、策略池，就不能修改。为了统计收益率。
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=16,blank=True,verbose_name="任务名") 
    desc = models.CharField(max_length=256,blank=True,verbose_name="任务描述")
    tasktype = models.CharField(max_length=16,blank=True,verbose_name="任务类型") #后面可能有共享任务，这个字段先保留
    strategyid = models.IntegerField(blank=True,null=True,verbose_name="策略id")
    stockpoolid = models.IntegerField(blank=True,null=True,verbose_name="股票池id")
    creatorid = models.CharField(max_length=32,blank=True,verbose_name="所属用户id")
    lastrun = models.CharField(max_length=20,blank=True,verbose_name="最后运行时间")
    runstatus = models.CharField(max_length=16,blank=True,verbose_name="运行状态")
    noticeid = models.IntegerField(blank=True,null=True,verbose_name="通知配置方案id")
    createtime = models.CharField(max_length=20,blank=True,verbose_name="创建时间")
    class Meta:
        # 设置表名
        db_table = "monitortask"
        verbose_name = "监控任务"  
        verbose_name_plural = verbose_name  #这个选项是指定，模型的复数形式
        abstract = False    #定义当前的模型是不是一个抽象类,抽象类不建数据库表，用于继承。
class noticeconfig(models.Model):   #收益率表
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=16,blank=True,verbose_name="通知方案名") 
    desc = models.CharField(max_length=256,blank=True,verbose_name="任务描述")
    creatorid = models.CharField(max_length=32,blank=True,verbose_name="所属用户id")
    method = models.CharField(max_length=32,blank=True,verbose_name="通知方案")    #email   wx   message
    email = models.CharField(max_length=32,blank=True,verbose_name="email")    #email   wx   message
    phonenum = models.CharField(max_length=32,blank=True,verbose_name="手机号")    #email   wx   message
    createtime = models.CharField(max_length=20,blank=True,verbose_name="创建时间")
    changetime = models.DateTimeField(auto_now = True,verbose_name="变更时间")
    class Meta:
        # 设置表名
        db_table = "noticeconfig"
        verbose_name = "通知方案配置"  
        verbose_name_plural = verbose_name  #这个选项是指定，模型的复数形式
        abstract = False    #定义当前的模型是不是一个抽象类,抽象类不建数据库表，用于继承。

class strategyyields(models.Model):   #收益率表
    id = models.AutoField(primary_key=True)
    strategyid = models.IntegerField(blank=True,null=True,verbose_name="策略id")
    stockpoolid = models.IntegerField(blank=True,null=True,verbose_name="绑定股票池id")
    yields = models.DecimalField(max_digits=7,decimal_places=4,blank=True,verbose_name="收益率")
    starttime = models.CharField(max_length=20,blank=True,verbose_name="起始时间")
    endtime = models.CharField(max_length=20,blank=True,verbose_name="终止时间")
    class Meta:
        # 设置表名
        db_table = "strategyyields"
        verbose_name = "策略收益"  
        verbose_name_plural = verbose_name  #这个选项是指定，模型的复数形式
        abstract = False    #定义当前的模型是不是一个抽象类,抽象类不建数据库表，用于继承。

class strategyorder(models.Model): #策略买卖订单
    id = models.AutoField(primary_key=True)
    strategyid = models.IntegerField(blank=True,null=True,verbose_name="策略id")
    buyerid = models.CharField(max_length=32,blank=True,verbose_name="买方id")
    sellerid = models.CharField(max_length=32,blank=True,verbose_name="卖方id")
    class Meta:
        # 设置表名
        db_table = "strategyorder"
        verbose_name = "策略模型交易订单"  
        verbose_name_plural = verbose_name  #这个选项是指定，模型的复数形式
        abstract = False    #定义当前的模型是不是一个抽象类,抽象类不建数据库表，用于继承。

'''
class indicators(models.Model): #指标标准库
    indicatorid = models.AutoField(primary_key=True)
    indicatorname = models.CharField(max_length=32,blank=False,verbose_name="指标名称")  #不区分前缀指标和后缀指标。通过运算表达式统一控制
    type = models.CharField(max_length=8,blank=False,verbose_name="指标类型")   #标准指标 or 自定义数值    standard   custom
    changetime = models.DateTimeField(auto_now = True,verbose_name="变更时间")
    desc = models.CharField(max_length=256,blank=False,verbose_name="指标描述")
    class Meta:
        # 设置表名
        db_table = "indicators"
        verbose_name = "指标标准库"  
        verbose_name_plural = verbose_name  #这个选项是指定，模型的复数形式
        abstract = False    #定义当前的模型是不是一个抽象类,抽象类不建数据库表，用于继承。
class indicatorexpression(models.Model): #指标表达式
    group = models.CharField(max_length=32,blank=False,verbose_name="指标组")
    strategyid = models.ForeignKey(strategypool,on_delete=models.PROTECT)
    prefixcoefficient = models.CharField(max_length=8,blank=False,null=True,verbose_name="前缀系数")
    prefixindicator = models.ForeignKey(indicators,on_delete=models.PROTECT,verbose_name="前缀指标",related_name="prefix")
    condition = models.CharField(max_length=32,blank=False,verbose_name="条件")
    suffixcoefficient = models.CharField(max_length=8,blank=False,null=True,verbose_name="后缀系数")
    suffixindicator = models.ForeignKey(indicators,on_delete=models.PROTECT,verbose_name="后缀指标",related_name="suffix")
    class Meta:
        # 设置表名
        db_table = "indicatorexpression"
        verbose_name = "指标表达式"  
        verbose_name_plural = verbose_name  #这个选项是指定，模型的复数形式
        abstract = False    #定义当前的模型是不是一个抽象类,抽象类不建数据库表，用于继承。
class filter(models.Model):  #过滤器表
    strategyid = models.ForeignKey(strategypool,on_delete=models.PROTECT)  
    userid = models.ForeignKey(usermanager,on_delete=models.PROTECT)
    type = models.CharField(max_length=8,blank=False,verbose_name="过滤器类别")  #前缀过滤器、买入过滤器等
    expression = models.CharField(max_length=256,blank=False,verbose_name="过滤器表达式")  #group1 & group2类似  这里没有再搞外键，担心表过于复杂。
    class Meta:
        # 设置表名
        db_table = "filter"
        verbose_name = "过滤器表"  
        verbose_name_plural = verbose_name  #这个选项是指定，模型的复数形式
        abstract = False    #定义当前的模型是不是一个抽象类,抽象类不建数据库表，用于继承。

#做个实验验证type方式创建类不继承内置方法/魔法方法,结果发现也继承，这里没搞懂为什么到里面就没有了module，google也没找到类似的最终答案：https://stackoverflow.com/questions/7320705/python-missing-class-attribute-module-when-using-type
print("start")
class demoA():
    a = 1

A = demoA()
print(A.__module__)

demoB = type("demoB",(demoA,),{"a":2,})
B = demoB()
print(demoB().__module__)
print(B.__module__)
print("end")
# 全局变量，用于记录新创建的Model类
models_dict = {}

'''
'''  原始写法写的比较优雅，这里保留下用作参考
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

'''

#在其他地方，从现网更新stock时，先判断是否有这个model了，没有则插入。
def createStockModel(name):
    #只允许从外面动态调用
    class Meta:
        db_table = name
        app_label = 'wxcloudrun'
        verbose_name = name
        verbose_name_plural = verbose_name
    attrs = {
        '__module__': '',
        'Meta': Meta,
        'date' : models.CharField(max_length=20,blank=False,primary_key=True,verbose_name="日期"),
        'open_cq' : models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="除权开盘价"),
        'high_cq' : models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="除权最高价"),
        'low_cq' : models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="除权最低价"),
        'close_cq' : models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="除权收盘价"),
        'open_hfq' : models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="后复权开盘价"),
        'high_hfq' : models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="后复权最高价"),
        'low_hfq' : models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="后复权最低价"),
        'close_hfq' : models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="后复权收盘价"),
        'volume' : models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="成交量"),
        'turnover' : models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="成交额"),
        'turnover_rate' : models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="换手率"),
        'change_rate' : models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="涨跌幅"),
        'amplitude' : models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="振幅"),
        'pre_volume' : models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="盘前成交量"),
        'pre_turnover' : models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="盘前成交额"),
        'pre_turnover_rate' : models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="盘前换手率"),
        'pre_change_rate' : models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="盘前涨跌幅"),
        'after_volume' : models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="盘后成交量"),
        'after_turnover' : models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="盘后成交额"),
        'after_turnover_rate' : models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="盘后换手率"),
        'after_change_rate' : models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="盘后涨跌幅--应该没有意义，盘后固定价格交易"),
        'suspension' : models.BooleanField(null=True,verbose_name="是否停牌。0否，1是"),
        'net_asset' : models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="资产净值"),
        'net_profit' : models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="净利润"),
        'earning_per_share' : models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="每股盈利"),
        'outstanding_shares' : models.IntegerField(blank=False,null=True,verbose_name="流通股本"),
        'net_asset_per_share' : models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="每股净资产"),
        'circular_market_val' : models.DecimalField(max_digits=20,decimal_places=4,blank=False,null=True,verbose_name="流通市值"),
        'data_check_flag' : models.CharField(max_length=20,blank=False,verbose_name="数据校验标志"),
        'data_last_check_date' : models.CharField(max_length=20,blank=False,verbose_name="最后一次校验时间"),
    }
    # 继承models.Model
    setattr(apps.get_app_config('wxcloudrun'), Meta.db_table, type(Meta.db_table, (models.Model,), attrs))
    '''
    if dynamicCall:
        call_command("makemigrations", interactive=False)
        call_command("migrate", interactive=False) 
    '''
    return  

def dynamicStockTable():
    stocks = stockbasicinfo.objects.all()
    for i in stocks:
        createStockModel("stock_"+i.stockcode)
#dynamicStockTable()
#createStockModel('000000')


'''
后面需要做自动migrate的时候，再研究下怎么触发。也可以通过命令行来触发，可能更简单。

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
    assert tableName.find(applabel) == -1
    if len(re.findall('\d\d\d\d\d\d',tableName)) != 0:
        doMigrate('stockdata_'+tableName,applabel,getFields('stockdata','list'))
        return
    #这里最好判断下是否创建成功。这里不能调用getModel判断，否则外层调用getModel，会死循环。
    doMigrate(tableName,applabel,getFields(applabel+'_'+tableName,'list'))
    #doMigrate('stockstaticdata','wxcloudrun',getFields('stockstaticdata','list'))
    #doMigrate('strategyconfig','wxcloudrun',getFields('strategyconfig','list'))
    #doMigrate('usermanager','wxcloudrun',getFields('usermanager','list'))
    #doMigrate('stockData',stockCQinfoFields)
'''
