from datetime import datetime

from django.db import models


# Create your models here.
class usermanager(models.Model): #model的meta有
    userid = models.CharField(max_length=32,blank=False,primary_key=True,verbose_name="用户id")  #这里用户id实际长度 28，如：oHqS86cHPMo7D0_2xb8pd6VranAU
    useraccount = models.CharField(max_length=32,blank=False,verbose_name="微信的账号用户名")
    username = models.CharField(max_length=32,blank=False,verbose_name="微信昵称")
    registtime = models.CharField(max_length=20,blank=False,verbose_name="注册时间")
    uuid = models.CharField(max_length=32,blank=False,verbose_name="用户标识")
    level = models.CharField(max_length=8,blank=False,verbose_name="用户等级")  #level 999 管理员 
    valid = models.BooleanField(null=True,verbose_name="生效状态")
    validtime = models.CharField(max_length=20,blank=False,verbose_name="截止有效时间")
    cashflow = models.IntegerField(blank=False,null=True,verbose_name="流水")
    class Meta:
        # 设置表名
        db_table = "usermanager"
        verbose_name = "用户管理"  
        verbose_name_plural = verbose_name  #这个选项是指定，模型的复数形式
        abstract = False    #定义当前的模型是不是一个抽象类,抽象类不建数据库表，用于继承。

class strategypool(models.Model):  #用户创建的量化策略，不指定primary，按照查阅资料，会自动增加一个自增id，而指定了则不会
    strategyname = models.CharField(max_length=16,blank=False,verbose_name="策略名") #策略名
    strategydesc = models.CharField(max_length=256,blank=False,verbose_name="策略描述")
    ownderid=models.ForeignKey(usermanager,on_delete=models.PROTECT,verbose_name="策略拥有者") #外键，CASCADE关联删除   PROTECT保护处理  SET_NULL置空处理  DO_NOTHING不处理
    creatorid = models.ForeignKey(usermanager,on_delete=models.PROTECT,verbose_name="策略创建者")   #随着策略交易，可能某些策略会属于不同的人。  通过策略拥有者和创建者一致性判断是否是购买的策略
    createtime = models.CharField(max_length=20,blank=False,verbose_name="创建时间")
    owntime = models.CharField(max_length=20,blank=False,verbose_name="归属时间")  #策略归属于拥有者的时间
    changetime = models.CharField(max_length=20,blank=False,verbose_name="变更时间") #策略被修改时间，可以是创建者或者拥有者
    validtime = models.CharField(max_length=20,blank=False,verbose_name="有效期") #策略可以以使用时间作为交易。
    runstatus = models.CharField(max_length=8,blank=False,verbose_name="策略运行状态")  #创建状态、回测状态、发布状态、下架状态、生效中等
    buyoutprice = models.IntegerField(blank=False,null=True,verbose_name="买断售价")  #买断：购买者可明文查看策略内容、编辑扩展等。
    unitprice = models.IntegerField(blank=False,null=True,verbose_name="购买时间单价")  #时间单价以交易日按天计算 
    protectlevel = models.IntegerField(blank=False,null=True,verbose_name="策略保护级别")  #购买者在买断后
    linkid = models.IntegerField(blank=False,null=True,verbose_name="绑定到某个策略") #当策略有linkid时，处于维护状态，以link过去的策略id作为实际策略。
    popular = models.IntegerField(blank=False,null=True,verbose_name="策略点赞热度")  #用户点赞热度。

class stockpool(models.Model):#股票池表，用户可以自定义股票池，用于应用不同策略
    poolname = models.CharField(max_length=16,blank=False,verbose_name="股票池名称") #策略名
    userid = models.ForeignKey(usermanager,on_delete=models.PROTECT)

class strategyyields(models.Model):   #收益率表
    poolname = models.ForeignKey(stockpool,on_delete=models.PROTECT)
    strategyid = models.ForeignKey(to=strategypool,to_field=id,on_delete=models.PROTECT)  #如果这么会报错的话就手动指定strategy的primary key和自增id
    yields = models.DecimalField(max_digits=7,decimal_places=4,blank=False,null=True,verbose_name="收益率")
    starttime = models.CharField(max_length=20,blank=False,verbose_name="起始时间")
    endtime = models.CharField(max_length=20,blank=False,verbose_name="终止时间")

class strategyorder(models.Model): #策略买卖订单
    strategyid = models.ForeignKey(to=strategypool,to_field=id,on_delete=models.PROTECT)
    userid = models.ForeignKey(usermanager,on_delete=models.PROTECT)

class indicators(models.Model): #指标标准库
    
    indicators = models.CharField(max_length=32,blank=False,verbose_name="指标or数值")  #不区分前缀指标和后缀指标。通过运算表达式统一控制
    desc = models.CharField(max_length=256,blank=False,verbose_name="描述")
class indicatorexpression(models.Model): #指标表达式
    group = models.CharField(max_length=32,blank=False,verbose_name="指标组")
    strategyid = models.ForeignKey(to=strategypool,to_field=id,on_delete=models.PROTECT)
    prefixindicator = models.CharField(max_length=32,blank=False,verbose_name="前缀指标")
    condition = models.CharField(max_length=32,blank=False,verbose_name="条件")
    suffixindicator = models.CharField(max_length=32,blank=False,verbose_name="前缀指标")

class filter(models.Model):  #过滤器表
    strategyid = models.ForeignKey(to=strategypool,to_field=id,on_delete=models.PROTECT)  
    userid = models.ForeignKey(usermanager,on_delete=models.PROTECT)
    type = models.CharField(max_length=8,blank=False,verbose_name="过滤器类别")  #前缀过滤器、买入过滤器等
    expression = models.CharField(max_length=256,blank=False,verbose_name="过滤器表达式")  #group1 & group2类似  这里没有再搞外键，担心表过于复杂。