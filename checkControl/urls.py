
from django.urls import path,include

from checkControl import views
appname = 'checkControl'
urlpatterns = [
    path("check_index/",views.check_index), #资产盘点
    path("insertCheck/",views.insertCheck), #添加盘点
    path("changeCheckStatus/<int:id>/",views.changeCheckStatus), #开始盘点
    path("deleteCheck/<int:id>/",views.deleteCheck), #删除盘点单

    path("check_show/",views.check_show), #查看盘点资产
    path("check_out/",views.check_out), #导出数据
    path("search_check/",views.search_check), #按资产编码查询

    
    path("checkUserManage/",views.checkUserManage), #盘点员管理
    path("insertCheckUser/",views.insertCheckUser), #添加盘点员
    path("update_checkUserManage/<int:id>/",views.update_checkUserManage), #修改盘点员信息
    path("deleteCheckUser/<int:id>/",views.deleteCheckUser), #删除盘点管理员

    path("scan/",views.scan),#钉钉扫码
    path("sc/",views.sc), #测试
    path("update_scan_info/<int:id>/<str:identy>/",views.update_scan_info), #修改被扫码资产信息
    path("get_access_token/",views.get_access_token),#获取登录用户的访问凭证
]