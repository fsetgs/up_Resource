from django.db import models
from userControl.models import *
# Create your models here.
# 资产名称表
class resourceName(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="资产名称",max_length=10)

# 资产类型表
class resourceType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="资产类型",max_length=50)
    code = models.CharField(verbose_name="类型编码",max_length=10)
    comment = models.CharField(verbose_name="备注",max_length=100,null=True)

# 资产状态表
class resourceStatus(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="资产状态",max_length=50)
    comment = models.CharField(verbose_name="备注",max_length=100,null=True)

# 资产来源表
class resourceFrom(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="资产来源",max_length=50)
    comment = models.CharField(verbose_name="备注",max_length=100,null=True)

# 存放区域表
class resourceLocation(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="资产存放区域",max_length=50)
    comment = models.CharField(verbose_name="备注",max_length=100,null=True)
    
# 计量单位
class resourceUnits(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="计量单位",max_length=50)
    comment = models.CharField(verbose_name="备注",max_length=100,null=True)

# 资产供应商
class resourceProvider(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="供应商",max_length=10)


# 资产信息表
class resourceInfo(models.Model):
    id = models.AutoField(primary_key=True)
    storage_time = models.CharField(verbose_name="入库时间",max_length=20,null=True,blank=True)
    buy_time = models.CharField(verbose_name="购买日期",max_length=20,null=True,blank=True)
    resource_price = models.CharField(verbose_name="资产原值",max_length=20,null=True,blank=True)
    depreciation_period = models.CharField(verbose_name="折旧周期",max_length=20,null=True,blank=True)
    residuals_rate = models.CharField(verbose_name="残值率",max_length=20,null=True,blank=True)
    resource_residuals = models.CharField(verbose_name="资产残值",max_length=20,null=True,blank=True)
    month_depreciation = models.CharField(verbose_name="月折旧额",max_length=20,null=True,blank=True)
    total_depreciation = models.CharField(verbose_name="累计折旧",max_length=20,null=True,blank=True)
    net_value = models.CharField(verbose_name="资产净值",max_length=20,null=True,blank=True)
    specifications = models.CharField(verbose_name="规格型号",max_length=50,null=True,blank=True)
    units = models.CharField(verbose_name="计量单位",max_length=20,null=True,blank=True)
    provider = models.CharField(verbose_name="供应商",max_length=50,null=True,blank=True)
    # product = models.CharField(verbose_name="制造商",max_length=20,null=True,blank=True)
    mac = models.CharField(verbose_name="MAC",max_length=50,null=True,blank=True)
    sn = models.CharField(verbose_name="SN号",max_length=50,null=True,blank=True)
    comment = models.CharField(verbose_name="备注",max_length=50,null=True,blank=True)

# 资产表
class resource(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="资产名",max_length=50,null=True,blank=True)
    code = models.CharField(verbose_name="资产编码",max_length=20,default="0")
    location = models.CharField(verbose_name="存放地点",max_length=100,null=True,blank=True)
    location_area = models.CharField(verbose_name="存放区域",max_length=100,null=True,blank=True)
    duty = models.CharField(verbose_name="责任人",max_length=20,null=True,blank=True)
    # user = models.ForeignKey(verbose_name="借用人",to=userInfo,to_field="id",on_delete=models.CASCADE,null=True,blank=True)
    user = models.CharField(verbose_name="借用人",max_length=20,null=True,blank=True)
    borrow_department = models.CharField(verbose_name="借用部门",max_length=20,null=True,blank=True)
    department = models.ForeignKey(verbose_name="所属部门",to=department,to_field="id",on_delete=models.CASCADE,null=True,blank=True)
    company = models.ForeignKey(verbose_name="所属公司",to=company,to_field="id",on_delete=models.CASCADE)
    # resource_type = models.CharField(verbose_name="资产类型",max_length=100,null=True,blank=True)
    resource_type = models.ForeignKey(verbose_name="类型展示",to=resourceType,to_field="id",on_delete=models.CASCADE,null=True,blank=True)
    resource_from = models.CharField(verbose_name="资产来源",max_length=100,null=True,blank=True)
    resource_status = models.CharField(verbose_name="资产状态",max_length=100,null=True,blank=True)
    borrow_time = models.CharField(verbose_name="借用时间",max_length=20,null=True,blank=True)
    return_time = models.CharField(verbose_name="预归还时间",max_length=20,null=True,blank=True)
    detail_info = models.ForeignKey(verbose_name="资产详情",to=resourceInfo,to_field="id",on_delete=models.CASCADE,null=True)


