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

class strategyPool(models.Model):  #用户创建的量化策略，不指定primary，按照查阅资料，会自动增加一个自增id，而指定了则不会
    strategyname = models.CharField(max_length=16,blank=False,verbose_name="策略名") #策略名
    ownderid=models.ForeignKey(usermanager,on_delete=models.PROTECT,verbose_name="策略拥有者") #外键，CASCADE关联删除   PROTECT保护处理  SET_NULL置空处理  DO_NOTHING不处理
    creatorid = models.ForeignKey(usermanager,on_delete=models.PROTECT,verbose_name="策略创建者")   #随着策略交易，可能某些策略会属于不同的人。
    createtime = models.CharField(max_length=20,blank=False,verbose_name="创建时间")
    owntime = models.CharField(max_length=20,blank=False,verbose_name="归属时间")  #策略归属于拥有者的时间
    changetime = models.CharField(max_length=20,blank=False,verbose_name="变更时间") #策略被修改时间，可以是创建者或者拥有者
    validtime = models.CharField(max_length=20,blank=False,verbose_name="有效期") #策略可以以使用时间作为交易。
    status = models.CharField(max_length=8,blank=False,verbose_name="策略状态")  #创建状态、回测状态、发布状态、下架状态、生效中等
    saleprice = models.IntegerField(blank=False,null=True,verbose_name="售价")  #当前暂定每个策略以买断状态为主。
    maintainlevel = models.CharField(max_length=8,blank=False,verbose_name="策略维护级别")  #策略交易后可以分为：不维护：策略以当时状态拷贝一份，创建者无需后续维护。维护：可以简单理解为这个只是个软连接，链接到创建者维护的策略，持续维护
    link = models.IntegerField(blank=False,null=True,verbose_name="绑定到某个策略") #当策略处于维护状态时，以link过去的策略为准。这里可以理解为只是一个软连接。

class stockpool(models.Model):#股票池表，用户可以自定义股票池，用于应用不同策略
    poolname = models.CharField(max_length=16,blank=False,verbose_name="股票池名称") #策略名
    userid = models.ForeignKey(usermanager,on_delete=models.PROTECT)

class strategyyields(models.Model):
    poolname = models.ForeignKey(stockpool,on_delete=models.PROTECT)
    strategyname = models.ForeignKey(strategyPool,on_delete=models.PROTECT)
    yields = models.DecimalField(max_digits=7,decimal_places=4,blank=False,null=True,verbose_name="收益率")
    starttime = models.CharField(max_length=20,blank=False,verbose_name="起始时间")
    endtime = models.CharField(max_length=20,blank=False,verbose_name="终止时间")

class strategyorder(models.Model): #策略买卖订单
    strategyname = models.ForeignKey(strategyPool,on_delete=models.PROTECT)
    userid = models.ForeignKey(usermanager,on_delete=models.PROTECT)