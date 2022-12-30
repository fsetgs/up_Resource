
from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from .models import *
from mainControl.views import paginator,get_access_token,get_user_info,get_userID
from userControl.models import *
from Resource.settings import *
from dataControl.models import *
import json,requests,datetime
from django.views.decorators.csrf import csrf_exempt
from checkControl.task import *
from django.core.cache import cache
from dataControl.views import search_paginator
# Create your views here.

def check_index(request):
    if request.method == "GET":
        # admin_list = []
        index_list = check.objects.all()
        # for check_obj in index_list:
        #     check_admins_obj = check_user.objects.filter(t_check=check_obj)
        #     for admin_obj in check_admins_obj:
        #         admin_list.append(admin_obj.t_user.real_name)
        return render(request,"c_index.html",paginator(request,index_list))

@csrf_exempt
def insertCheck(request):
    if request.method == "GET":
        company_obj = company.objects.all()
        return render(request,"c_insert.html",locals())
    if request.method == "POST":
        check_name = request.POST.get("check_name")
        user_name = request.POST.get("user_name")
        user_phone = request.POST.get("user_phone")
        company_name = request.POST.get("company")
        print("获取insert数据",check_name,user_name,user_phone,company_name)
        is_check = check.objects.filter(name=check_name)
        if is_check:
            return HttpResponse("<h1>已存在同名盘点单，请勿重复创建！</h1>")
        if company_name:
            if not check_name:
                date = datetime.date.today()
                check_name = str(date.year)+"年"+str(date.month)+"月"+str(date.day)+ "日-" + company_name + "盘点单"
            check_obj = check.objects.create(name=check_name,check_company=company_name)
            if user_name and user_phone:
                check_admin.objects.create(t_check=check_obj,name=user_name,phone=user_phone)
            return HttpResponse("<h1>创建完成，刷新页面即可。</h1>")
        return HttpResponse("<h1>请选择盘点的公司。</h1>")

def checkUserManage(request):
    if request.method == "GET":
        index_list = check_admin.objects.all()
        return render(request,"checkUserManage.html",paginator(request,index_list))

@csrf_exempt
def insertCheckUser(request):
    if request.method == "GET":
        check_obj = check.objects.all()
        return render(request,"insertCheckUser.html",locals())
    if request.method == "POST":
        print("插入管理员：",request.POST)
        check_name = request.POST.get("check_name")
        user_name = request.POST.get("user_name")
        user_phone = request.POST.get("user_phone")
        check_obj = check.objects.get(name=check_name)
        check_admin.objects.create(t_check=check_obj,name=user_name,phone=user_phone)
        return HttpResponse("<h1>添加成功</h1>")

def update_checkUserManage(request,id):
    id = int(id)
    if request.method == "GET":
        check_obj = check.objects.all()
        adminUser_obj = check_admin.objects.get(id=id)
        return render(request,"updateCheckUser.html",locals())
    if request.method == "POST":
        check_name = request.POST.get("check_name")
        user_name = request.POST.get("user_name")
        user_phone = request.POST.get("user_phone")
        comment = request.POST.get("comment")
        check_obj = check.objects.get(name=check_name)
        adminUser_obj = check_admin.objects.get(id=id)
        adminUser_obj.t_check = check_obj
        adminUser_obj.name = user_name
        adminUser_obj.phone = user_phone
        adminUser_obj.save()
        return HttpResponse("<h1>修改成功，刷新页面即可。</h1>")

def deleteCheckUser(requeset,id):
    if requeset.method == "GET":
        admin_obj = check_admin.objects.get(id=id)
        admin_obj.delete()
        return redirect(to="/check/checkUserManage/")



def changeCheckStatus(request,id):
    if request.method == "GET":
        check_obj = check.objects.get(id=id)
        check_status = check_obj.status
        if check_status == "0":
            addcheck.delay(check_obj.check_company,id)
            check_obj.status = "1"
        elif check_status == "1":
            stopcheck.delay(id)
            check_obj.status = "2"
        check_obj.save()
        return redirect(to="/check/check_index/")

def deleteCheck(request,id):
    if request.method == "GET":
        check.objects.get(id=id).delete()
        deletecheck.delay(id)
        return redirect(to="/check/check_index/")





def check_show(request):
    if request.method == "GET":
        check_obj = check_resource.objects.all().order_by("-id")
        return render(request,"checked_index.html",paginator(request,check_obj))

@csrf_exempt
def check_out(request):
    if request.method == "GET":
        check_obj = check.objects.all()
        return render(request,"check_out.html",locals())
    if request.method == "POST":
        data = {}
        check_out_id = request.POST.get("check")
        check_status = request.POST.get("status")
        if check_out_id == "":
            data["message"] = "请选择盘点单"
            return JsonResponse(data,safe=False)

        if check_status == "all":
            relate_obj = check_resource.objects.filter(t_check_id=check_out_id)
        else:
            relate_obj = check_resource.objects.filter(t_check_id=check_out_id,is_checked=check_status)
        print(check_out_id,relate_obj)
        if relate_obj:
            upfile_url = MEDIA_ROOT + '/tempUpfile/' + relate_obj[0].t_check.name + ".xlsx"
            wb = Workbook()
            wb.create_sheet(index=0,title="Sheet1")
            ws = wb.active
            ws['A1'] = '所属盘点'
            ws['B1'] = '资产编码'
            ws['C1'] = '资产名称'
            ws['D1'] = '盘点状态'
            for i in range(len(relate_obj)):
                ws[f'A{i+2}'] = relate_obj[i].t_check.name
                ws[f'B{i+2}'] = relate_obj[i].t_resource.code
                ws[f'C{i+2}'] = relate_obj[i].t_resource.name
                ws[f'D{i+2}'] = relate_obj[i].is_checked
            wb.save(upfile_url)
            data["message"] = "success"
            data["url"] = '/media/tempUpfile/' + relate_obj[0].t_check.name + ".xlsx"
        
        data["message"] = "failed"
        return JsonResponse(data,safe=False)

def search_check(request):
    if request.method == "GET":
        search_paginator_code = request.GET.get("code")
        print("分页时获取参数：",search_paginator_code)
        if search_paginator_code:
            method = request.GET.get("method")
            code = request.GET.get("code")
            if method == "get":
                res_obj = resource.objects.get(code=code)
                index_list = check_resource.objects.filter(t_resource=res_obj)
                method = "get"
            elif method == "post":
                index_list = check_resource.objects.filter(is_checked=code)
                method = "post"
        else:
            code = request.GET.get("search1")
            try:
                res_obj = resource.objects.get(code=code)
                index_list = check_resource.objects.filter(t_resource=res_obj)
            except:
                index_list = []
            method = "get"
        code = code
    if request.method == "POST":
        status = request.POST.get("search2")
        index_list = check_resource.objects.filter(is_checked=status)
        code = status
        method = "post"
    return render(request,"checked_index.html",search_paginator(request,index_list,code,method))


#调用钉钉扫码
def scan(request):
    if request.method == "GET":
        code = request.GET.get("code") #免登授权码
        message = request.GET.get("message") #该信息为接口返回的资产编码
        err = request.GET.get("err") #扫码失败
        if code:
            access_token = cache.get("access_token")
            try:
                user_id,scan_name = get_userID(request,access_token,code)
            except:
                access_token = get_access_token(request)
                user_id,scan_name = get_userID(request,access_token,code)

            if user_id: #获取扫码人的个人详情
                scan_name,phone = get_user_info(request,access_token,user_id)
        if message:
            try:
                res_obj = resource.objects.get(code=message)    
                try:
                    # 管理员入口
                    check_obj = check_resource.objects.get(t_resource=res_obj).t_check
                    admin = check_admin.objects.get(name=scan_name,phone=phone,t_check=check_obj)
                    if admin:        
                        type_obj = resourceType.objects.all()
                        from_obj  =resourceFrom.objects.all()
                        status_obj = resourceStatus.objects.all()
                        company_obj = company.objects.all()
                        department_obj = department.objects.filter(company=res_obj.company)
                        company_department = {}
                        for companys in company_obj:
                            department_list = []
                            department_objs = department.objects.filter(company=companys)
                            for i in department_objs:
                                department_list.append(i.name)
                            company_department[companys.name] = department_list
                        
                        aaa = json.dumps(company_department)
                        print("AB",aaa)

                        return render(request,"resource_admin_check.html",locals())
                except:
                    # 员工个人入口
                    return render(request,"resource_check.html",locals())
            except:
                return HttpResponse("<h1>该资产可能未入库</h1>")
        if err:
            print(err)
            return HttpResponse("<h1>扫码失败！</h1>")
        return render(request,'scan.html',locals())

def sc(request):
    res_obj = resource.objects.get(code="0302DMT1904060")    
    type_obj = resourceType.objects.all()
    from_obj  =resourceFrom.objects.all()
    status_obj = resourceStatus.objects.all()
    company_obj = company.objects.all()
    department_obj = department.objects.filter(company=res_obj.company)
    return render(request,"resource_admin_check.html",locals())
        
# @csrf_exempt
def update_scan_info(request,id,identy):
    if request.method == "GET":
        try:
            res_obj = resource.objects.get(id=id)
        except:
            return HttpResponse("<h1>该资产不存在。</h1>")
        if identy == "user":
            borrow_user = request.GET.get("borrow_user")
            res_obj.user = borrow_user
        if identy == "admin":
            resource_name = request.GET.get("resource_name")
            companys = request.GET.get("company")
            departments = request.GET.get("department")
            duty_user = request.GET.get("duty_user")
            resource_status = request.GET.get("resource_status")
            if resource_status == "在用":
                borrow_department = request.GET.get("borrow_department")
                borrow_user = request.GET.get("borrow_user")
            else:
                borrow_department = ""
                borrow_user = ""
            location_area = request.GET.get("location_area")
            location = request.GET.get("location")
            specifications = request.GET.get("specifications")
            try:
                company_obj = company.objects.get(name=companys)
                res_obj.company = company_obj
            except:
                return HttpResponse("<h1>公司不存在</h1>")
            try:
                department_obj = department.objects.get(name=departments,company=company_obj)
                res_obj.department = department_obj
            except Exception as e:
                print(e)
            res_obj.name = resource_name
            res_obj.duty = duty_user
            res_obj.resource_status = resource_status
            res_obj.borrow_department = borrow_department
            res_obj.user = borrow_user
            res_obj.location_area = location_area
            res_obj.location = location
            res_obj.detail_info.specifications = specifications
            res_obj.detail_info.save()
        res_obj.save()
        try:
            check_resobj = check_resource.objects.get(t_resource=res_obj)
            if check_resobj.is_checked == "未盘点":
                return HttpResponse("<h1>修改失败！本次盘点已结束。</h1>")
            check_resobj.is_checked = "已盘点"
            check_resobj.save()
        except:
            return HttpResponse("<h1>该资产表已不存在</h1>")
        return HttpResponse("<h1>该资产已完成盘点</h1>")