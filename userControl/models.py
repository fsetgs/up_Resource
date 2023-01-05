
from django.db import models

# Create your models here.

# 公司表
class company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="公司名称",max_length=50,null=True,blank=True)
    code = models.CharField(verbose_name="编码",max_length=10,null=True,blank=True)
    is_header = models.CharField(verbose_name="是否为总部",max_length=5,default="0") # 0不是 1是
    comment = models.CharField(verbose_name="备注",max_length=50,null=True,blank=True)
    

# 部门表
class department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="部门名称",max_length=20,null=True,blank=True)
    code = models.CharField(verbose_name="编码",max_length=10,null=True,blank=True)
    company=models.ForeignKey(verbose_name="所属公司",to=company,to_field="id",on_delete=models.CASCADE,null=True,blank=True)
    comment = models.CharField(verbose_name="备注",max_length=50,null=True,blank=True)

# 用户信息表
class userInfo(models.Model):
    id = models.AutoField(primary_key=True)
    real_name = models.CharField(verbose_name='真实姓名',max_length=20)
    username = models.CharField(verbose_name='用户名',max_length=200)
    password = models.CharField(verbose_name='密码',max_length=50)
    phone = models.CharField(verbose_name='手机号',max_length=20)
    department = models.CharField(verbose_name='所属部门',max_length=20,null=True,blank=True)
    company = models.CharField(verbose_name='所属公司',max_length=20,null=True,blank=True)
    level = models.CharField(verbose_name="管理等级",max_length=5,default="0") # 0代表总公司权限 1代表拥有分公司权限
    comment = models.CharField(verbose_name="备注",max_length=50,null=True)

