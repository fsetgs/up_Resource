from django.db import models
from userControl.models import *
from dataControl.models import *
# Create your models here.
# 资产盘点表（记录每次盘点）
class check(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="表单名",max_length=30)
    status = models.CharField(verbose_name="盘点状态",max_length=10,default="0")
    check_company = models.CharField(verbose_name="盘点公司",max_length=20,blank=True,null=True)
    time = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    comment = models.CharField(verbose_name="备注",max_length=20,blank=True,null=True)

# 资产盘点关联表（将每张资产盘点表与资产关联起来）
class check_resource(models.Model):
    id = models.AutoField(primary_key=True)
    t_check = models.ForeignKey(verbose_name="资产盘点表",to=check,to_field="id",on_delete=models.CASCADE)
    t_resource = models.ForeignKey(verbose_name="资产表",to=resource,to_field="id",on_delete=models.CASCADE)
    is_checked = models.CharField(verbose_name="是否已盘",max_length=10,default="0") # 0代表盘点中 1代表已盘 2代表未盘

# 盘点管理员表
class check_admin(models.Model):
    id = models.AutoField(primary_key=True)
    t_check = models.ForeignKey(verbose_name="盘点表",to=check,to_field="id",on_delete=models.CASCADE)
    name = models.CharField(verbose_name="盘点员姓名",max_length=20,blank=True,null=True)
    phone = models.CharField(verbose_name="盘点员手机号",max_length=20,null=True,blank=True)