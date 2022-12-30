
from django.urls import path,include
from . import views
app_name='dataControl'
urlpatterns = [
    path("data_show/",views.data_show), #资产展示
    path("insertData/",views.insertData), #添加资产
    path("search_resource/",views.search_resource), #按资产搜索
    path("detail_show/<int:id>/",views.detail_show), #详情展示
    path("two_action/",views.two_action), #二级联动
    path("makeqr/<int:id>/",views.makeqr), #生成二维码
    path("updateData/<int:id>/",views.updateData), #更改资产信息
    path("deleteResource/<int:id>/",views.deleteResource), #删除资产
    
    path("up_fileData/",views.up_fileData), #快速上传资产信息

    path("borrow_show/",views.borrow_show), #资产借用展示
    path("search_borrowResource/",views.search_borrowResource), #借用资产查询
    path("returnResource/<int:id>",views.returnResource), #归还资产

    path("type_show/",views.type_show),#资产类型展示
    path("insert_type/",views.insert_type), #添加资产类型
    path("search_type/",views.search_type), #资产类型查询
    path("update_type/<int:id>/",views.update_type), #修改资产类型
    path("delete_type/<int:id>/",views.delete_type), #删除资产类型

    path("company_show/",views.company_show), #公司展示
    path("insert_company/",views.insert_company), #添加公司
    path("search_company/",views.search_company), #公司查询
    path("update_company/<int:id>/",views.update_company), #修改公司
    path("delete_company/<int:id>/",views.delete_company), #删除公司

    path("department_show/",views.department_show), #部门展示
    path("search_department/",views.search_department), #查询部门
    path("insert_department/",views.insert_department), #新增展示
    path("update_department/<int:id>/",views.update_department), #修改部门
    path("delete_department/<int:id>/",views.delete_department), #删除部门
]