from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from .models import *
from userControl.views import paginator
from userControl.models import *
from django.views.decorators.csrf import csrf_exempt
from Resource.settings import *
import json,requests,qrcode
from .task import *
from dingtalk import SecretClient
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger,InvalidPage
# Create your views here.

# 封装查询分页器,避免代码太多重复
def search_paginator(request,index_list,code,method):
    lenlist = len(index_list)
    paginator = Paginator(index_list,13)
    current_page = request.GET.get("page",1)
    page = int(current_page)
    # 固定显示7页，当大于7页时
    if paginator.num_pages > 7:
        if page-3 < 1:
            pageRange = range(1,8)
        elif page+3 > paginator.num_pages:
            pageRange = range(paginator.num_pages-6,paginator.num_pages+1)
        else:
            pageRange = range(page-3,page+4)
    else:
        pageRange = paginator.page_range

    try:
        obj_list = paginator.page(page)
    except PageNotAnInteger:
        obj_list = paginator.page(1)
    except InvalidPage:
        return HttpResponse('error')
    except EmptyPage:
        obj_list = paginator.page(paginator.num_pages)
    return {"lenlist":lenlist,"pageRange":pageRange,"index_list":obj_list,"code":code,"method":method}

# 数据采集展示
def data_show(request):
    if request.method == "GET":
        resource_obj = resource.objects.all().order_by("-id")
        return render(request,"dataShow.html",paginator(request,resource_obj))

# 添加资产
@csrf_exempt
def insertData(request):
    if request.method == "GET":
        company_obj = company.objects.all()
        department_obj = department.objects.all()
        localtion_area = resourceLocation.objects.all()
        type_obj = resourceType.objects.all()
        from_obj = resourceFrom.objects.all()
        status_obj = resourceStatus.objects.all()
        resourcename_obj = resourceName.objects.all()
        units_obj = resourceUnits.objects.all()
        provider_obj = resourceProvider.objects.all()
        return render(request,"insertData.html",locals())
    if request.method == "POST":
        print("资产插入POST提交",request.POST)
        resource_residuals = ""
        month_depreciation = ""
        total_depreciation = ""
        net_value = ""
        resource_name = request.POST.get("resource_name") #资产名称
        type_id = request.POST.get("resource_type") #资产分类
        resource_from = request.POST.get("resource_from") #资产来源
        resource_status = request.POST.get("resource_status") #资产状态
        companys = request.POST.get("company") #所属公司
        departments = request.POST.get("department") #所属部门
        duty = request.POST.get("duty_user") #责任所有人
        location_area = request.POST.get("location_area") #存放区域
        location = request.POST.get("location") #存放地点
        storage_time = request.POST.get("storage_time") #入库日期
        buy_time = request.POST.get("buy_time") #购置日期
        resource_price = request.POST.get("resource_price") #资产原值
        depreciation_period = request.POST.get("depreciation_period") #折旧周期
        residuals_rate = request.POST.get("residuals_rate") #残值率
        # resource_residuals = request.POST.get("resource_residuals") #资产残值
        specifications = request.POST.get("specifications") #规格型号
        units = request.POST.get("units") #计量单位
        # level =request.POST.get("level") #等级
        provider = request.POST.get("provider") #供应商
        # product = request.POST.get("product") #生产商
        sn = request.POST.get("sn") #SN号
        mac = request.POST.get("mac") #MAC
        comment = request.POST.get("comment")
        borrow_department = request.POST.get("borrow_department")
        borrow_user = request.POST.get("borrow_user")
        borrow_time = request.POST.get("borrow_time")
        return_time = request.POST.get("return_time")
        addnum = request.POST.get("addnum")
        if resource_name=="" or type_id=="" or resource_from=="" or resource_status=="" or companys=="" or departments=="" or location_area=="" or location=="" or storage_time=="" or buy_time=="" or units=="" or duty == "":
            return HttpResponse("<h1>所有*为必填项。</h1>")
        # if resource_status == "在用":
        #     if borrow_department == "" or borrow_user == "" or borrow_time == "" or return_time == "":
        #         return HttpResponse("<h1>若要使用该资产，借用信息为必填项。</h1>")
        try:
            company_obj = company.objects.get(name=companys)
        except Exception as e:
            print(e)
            return HttpResponse("<h1>该公司可能不存在</h1>")

        try:
            department_obj = department.objects.get(name=departments,company=company_obj)
        except Exception as e:
            print(e)
            return HttpResponse("<h1>该部门可能不存在</h1>")

        try:
            type_obj = resourceType.objects.get(id=int(type_id))
        except Exception as e:
            print(e)
            return HttpResponse("<h1>该类型可能不存在</h1>")

        # 计算资产残值、月折旧额、累计折旧、资产净值
        if resource_price != "" and depreciation_period != "" and residuals_rate != "":
            resource_residuals = str(int(resource_price)*int(residuals_rate)/100)
            month_depreciation = round(int(resource_price)*(1-int(residuals_rate)/100)/int(depreciation_period),2)
            storage_date = datetime.datetime.strptime(storage_time,"%Y-%m-%d")
            months = rrule.rrule(rrule.MONTHLY,dtstart=storage_date,until=datetime.datetime.now()).count()
            if months <= int(depreciation_period):
                total_depreciation = str(months*int(month_depreciation))
            else:
                total_depreciation = str(int(month_depreciation)*int(depreciation_period))
            net_value = str(int(resource_price)-int(total_depreciation))

        try:
            for i in range(int(addnum)):
                resInfo_obj = resourceInfo.objects.create(storage_time=storage_time,buy_time=buy_time,resource_price=resource_price,depreciation_period=depreciation_period,
                residuals_rate=residuals_rate,resource_residuals=resource_residuals,month_depreciation=month_depreciation,total_depreciation=total_depreciation,net_value=net_value
                ,specifications=specifications,units=units,provider=provider,mac=mac,sn=sn,comment=comment)

                res_obj = resource.objects.create(name=resource_name,resource_type=type_obj,resource_from=resource_from,resource_status=resource_status,duty=duty,
                company=company_obj,location_area=location_area,location=location,detail_info=resInfo_obj,user=borrow_user,department=department_obj,borrow_time=borrow_time,
                return_time=return_time,borrow_department=borrow_department)

                # 创建编码 公司编码+资产类型编码+部门编码+采购年月+顺序号（id）
                res_num = res_obj.id
                if len(str(res_num)) < 2:
                    num = "00" + str(res_num)
                elif 1 < len(str(res_num)) < 3:
                    num = "0" + str(res_num)
                elif 2 < len(str(res_num)):
                    num = str(res_num)
                resource_code = company_obj.code + type_obj.code + department_obj.code + buy_time[2:4] +buy_time[5:7] + num
                res_obj.code=resource_code
                res_obj.save()

            return HttpResponse("<h1>数据插入成功,刷新页面即可。</h1>")
        except Exception as e:
            print(e)
            return HttpResponse("<h1>数据插入失败,尝试添加完整信息。</h1>")

def search_resource(request):
    if request.method == "GET":
        search_paginator_code = request.GET.get("code")
        if search_paginator_code:
            method = request.GET.get("method")
            code = request.GET.get("code")
            if method == "get":
                index_list = resource.objects.filter(code__icontains=code)
                method = "get"
            elif method == "post":
                index_list = resource.objects.filter(name__icontains=code)
                method = "post"
        else:
            code = request.GET.get("search1")
            index_list = resource.objects.filter(code__icontains=code)
            method = "get"
        code = code
    if request.method == "POST":
        name = request.POST.get("search2")
        index_list = resource.objects.filter(name__icontains=name)
        code = name
        method = "post"
    return render(request,"dataShow.html",search_paginator(request,index_list,code,method))

# 资产细节查看
@csrf_exempt
def detail_show(request,id):
    if request.method == "GET":
        res_obj = resource.objects.get(id=id)
        type_obj = resourceType.objects.all()
        from_obj  =resourceFrom.objects.all()
        status_obj = resourceStatus.objects.all()
        company_obj = company.objects.all()
        department_obj = department.objects.filter(company=res_obj.company)
        return render(request,"detail_show.html",locals())
    if request.method == "POST":
        company_name = request.POST.get("company_name")
        print("公司查询",company_name)
        company_obj = company.objects.get(name=company_name)
        depantment_obj = department.objects.filter(company=company_obj)
        result = {}
        num = 0
        for obj in depantment_obj:
            result[f"{num}"] = obj.name
            num += 1
        return JsonResponse(result)

@csrf_exempt
def two_action(request):
        if request.method=="GET":
            company_name = request.GET.get("company_name")
            print("公司查询00",company_name)
            company_obj = company.objects.get(name=company_name)
            depantment_obj = department.objects.filter(company=company_obj)
            result = {}
            num = 0
            for obj in depantment_obj:
                result[f"{num}"] = obj.name
                num += 1
            return JsonResponse(result)

# 生成二维码
def makeqr(request,id):
    if request.method == "GET":
        res_obj = resource.objects.get(id=id)
        img = qrcode.make(f'http://120.78.177.255:8801/data/detail_show/{id}')
        img_url = "/QR_img/" + res_obj.code + '.jpg'
        save_path = MEDIA_ROOT + img_url
        img.save(save_path)
        return render(request,'qrshow.html',locals())

def updateData(request,id):
        if request.method == "POST":
            resource_name = request.POST.get("resource_name") #资产名称
            type_id = request.POST.get("resource_type") #资产分类
            resource_from = request.POST.get("resource_from") #资产来源
            resource_status = request.POST.get("resource_status") #资产状态
            companys = request.POST.get("company") #所属公司
            departments = request.POST.get("department")
            duty = request.POST.get("duty_user") #责任所有人
            location_area = request.POST.get("location_area") #存放区域
            location = request.POST.get("location") #存放地点
            storage_time = request.POST.get("storage_time") #入库日期
            buy_time = request.POST.get("buy_time") #购置日期
            resource_price = request.POST.get("resource_price") #资产原值
            depreciation_period = request.POST.get("depreciation_period") #折旧周期
            residuals_rate = request.POST.get("residuals_rate") #残值率
            # resource_residuals = request.POST.get("resource_residuals") #资产残值
            specifications = request.POST.get("specifications") #规格型号
            units = request.POST.get("units") #计量单位
            # level = request.POST.get("level") #等级
            provider = request.POST.get("provider") #供应商
            # product = request.POST.get("product") #制造商
            sn = request.POST.get("sn") #SN号
            mac = request.POST.get("mac")
            comment = request.POST.get("comment")
            if resource_status == "在用":
                borrow_department = request.POST.get("borrow_department")
                borrow_user = request.POST.get("borrow_user")
                borrow_time = request.POST.get("borrow_time")
                return_time = request.POST.get("return_time")
            else:
                borrow_department = ""
                borrow_user = ""
                borrow_time = ""
                return_time = ""
            try:
                company_obj = company.objects.get(name=companys)
            except:
                return HttpResponse("<h1>公司不存在</h1>")

            try:
                department_obj = department.objects.get(name=departments,company=company_obj)
            except:
                return HttpResponse("<h1>该公司部门不存在</h1>")
            try:
                type_obj = resourceType.objects.get(id=type_id)
            except:
                return HttpResponse("<h1>该类型不存在</h1>")

             # 计算资产残值、月折旧额、累计折旧、资产净值
            if resource_price != "" and depreciation_period != "" and residuals_rate != "":
                resource_residuals = str(int(resource_price)*int(residuals_rate)/100)
                month_depreciation = round(int(resource_price)*(1-int(residuals_rate)/100)/int(depreciation_period),2)
                storage_date = datetime.datetime.strptime(storage_time,"%Y-%m-%d")
                months = rrule.rrule(rrule.MONTHLY,dtstart=storage_date,until=datetime.datetime.now()).count()
                if months <= int(depreciation_period):
                    total_depreciation = str(months*int(month_depreciation))
                else:
                    total_depreciation = str(int(month_depreciation)*int(depreciation_period))
                net_value = str(int(resource_price)-int(total_depreciation))
            # 创建编码 公司编码+资产类型编码+部门编码+采购年月+顺序号（id）
            # res_num = id
            # if len(str(res_num)) < 2:
            #     num = "00" + str(res_num)
            # elif 1 < len(str(res_num)) < 3:
            #     num = "0" + str(res_num)
            # elif 2 < len(str(res_num)):
            #     num = str(res_num)
            # resource_code = company_obj.code + type_obj.code + department_obj.code + buy_time[2:4] +buy_time[5:7] + num

            try:
                resource.objects.filter(id=id).update(name=resource_name,resource_type=type_obj,resource_from=resource_from,resource_status=resource_status,
                company=company_obj,duty=duty,location_area=location_area,location=location,user=borrow_user,department=department_obj,borrow_time=borrow_time,
                return_time=return_time,borrow_department=borrow_department)

                resInfo_obj = resource.objects.get(id=id).detail_info
                resInfo_obj.storage_time = storage_time
                resInfo_obj.buy_time = buy_time
                resInfo_obj.resource_price = resource_price
                resInfo_obj.depreciation_period = depreciation_period
                resInfo_obj.residuals_rate = residuals_rate
                resInfo_obj.resource_residuals = resource_residuals
                resInfo_obj.month_depreciation = month_depreciation
                resInfo_obj.total_depreciation = total_depreciation
                resInfo_obj.net_value = net_value
                resInfo_obj.specifications = specifications
                resInfo_obj.units = units
                resInfo_obj.provider = provider
                resInfo_obj.sn = sn
                resInfo_obj.mac = mac
                resInfo_obj.comment = comment
                resInfo_obj.save()

                return HttpResponse("<h1>数据更改成功,刷新页面即可。</h1>")
            except Exception as e:
                print(e)
                return HttpResponse("<h1>数据更改失败,尝试添加完整信息。</h1>")
# 删除资产
def deleteResource(request,id):
    if request.method == "GET":
        try:
            res_obj = resource.objects.get(id=id)
            res_info_obj = res_obj.detail_info
            os.remove(MEDIA_ROOT + f'/QR_img/{res_obj.code}.jpg')
            res_info_obj.delete()
            res_obj.delete()
            return redirect(to="/data/data_show/")
        except:
            return redirect(to="/data/data_show/")

@csrf_exempt
def up_fileData(request):
    if request.method == "GET":
        return render(request,"up_fileData.html")
    if request.method == "POST":
        files = request.FILES.getlist("file")
        updata.delay(files)
        return_data = {}
        return_data["message"] = "数据转移中，可先进行其它操作。"
        json_message = json.dumps(return_data)
        return HttpResponse(json_message)

def borrow_show(request):
    if request.method == "GET":
        res_obj = resource.objects.filter(resource_status="在用").order_by("-borrow_time")
        return render(request,"borrow_show.html",paginator(request,res_obj))

# 借用资产查询
def search_borrowResource(request):
    if request.method == "GET":
        search_paginator_code = request.GET.get("code")
        if search_paginator_code:
            method = request.GET.get("method")
            code = request.GET.get("code")
            if method == "get":
                index_list = resource.objects.filter(name__contains=code).order_by("-id")
                method = "get"
            elif method == "post":
                index_list = resource.objects.filter(user__contains=code).order_by("-id")
                method = "post"
        else:
            code = request.GET.get("search1")
            index_list = resource.objects.filter(name__contains=code).order_by("-id")
            # index_list = resource.objects.filter(code__icontains=code)
            method = "get"
        code = code
    if request.method == "POST":
        search_user = request.POST.get("search2")
        index_list = resource.objects.filter(user__contains=search_user).order_by("-id")
        # index_list = resource.objects.filter(name__icontains=name)
        code = search_user
        method = "post"
    return render(request,"borrow_show.html",search_paginator(request,index_list,code,method))

        
# 资产归还
def returnResource(request,id):
    if request.method == "GET":
        res_obj = resource.objects.get(id=id)
        res_obj.user = ""
        res_obj.borrow_department = ""
        res_obj.resource_status = "闲置"
        res_obj.borrow_time = ""
        res_obj.return_time = ""
        res_obj.save()
        return redirect(to="/data/borrow_show/")

# 资产类型展示
def type_show(request):
    if request.method == "GET":
        type_obj = resourceType.objects.all()
        return render(request,"type_show.html",paginator(request,type_obj))

def insert_type(request):
    if request.method == "GET":
        return render(request,"insert_type.html",locals())
    if request.method == "POST":
        type_name = request.POST.get("type_name")
        type_code = request.POST.get("type_code")
        if type_name == "" or type_code == "":
            return HttpResponse("<h1>两项必填，不可为空。</h1>")
        resourceType.objects.create(name=type_name,code=type_code)
        return HttpResponse("<h1>操作成功，刷新页面即可。</h1>")

def search_type(request):
    if request.method == "GET":
        type_name = request.GET.get("search1")
        type_obj = resourceType.objects.filter(name__icontains=type_name)
    if request.method == "POST":
        type_code = request.POST.get("search2")
        type_obj = resourceType.objects.filter(code__icontains=type_code)
    return render(request,"type_show.html",paginator(request,type_obj))


def update_type(request,id):
    type_obj = resourceType.objects.get(id=id)
    if request.method == "GET":
        return render(request,"updateType.html",locals())
    if request.method == "POST":
        type_name = request.POST.get("type_name")
        type_code = request.POST.get("type_code")
        if type_name == "" or type_code == "":
            return HttpResponse("<h1>两项必填，不可为空。</h1>")
        type_obj.name = type_name
        type_obj.code = type_code
        type_obj.save()
        return HttpResponse("<h1>修改成功，刷新页面即可。</h1>")

def delete_type(request,id):
    if request.method == "GET":
        type_obj = resourceType.objects.get(id=id)
        type_obj.delete()
        return redirect(to="/data/type_show/")

def company_show(request):
    if request.method == "GET":
        company_obj = company.objects.all()
        return render(request,"company_show.html",paginator(request,company_obj))

def insert_company(request):
    if request.method == "GET":
        return render(request,"insert_company.html")
    if request.method == "POST":
        name = request.POST.get("company_name")
        code = request.POST.get("company_code")
        if name == "" or code == "":
            return HttpResponse("<h1>两项必填，不可为空。</h1>")
        company.objects.create(name=name,code=code)
        return HttpResponse("<h1>操作成功，刷新页面即可。</h1>")

def search_company(request):
    if request.method == "GET":
        company_name = request.GET.get("search1")
        company_obj = company.objects.filter(name__icontains=company_name)
    if request.method == "POST":
        company_code = request.POST.get("search2")
        company_obj = company.objects.filter(code__icontains=company_code)
    return render(request,"company_show.html",paginator(request,company_obj))
        

def update_company(request,id):
    company_obj = company.objects.get(id=id)
    if request.method == "GET":
        return render(request,"updateCompany.html",locals())
    if request.method == "POST":
        name = request.POST.get("company_name")
        code = request.POST.get("company_code")
        if name == "" or code == "":
            return HttpResponse("<h1>两项必填，不可为空。</h1>")
        company_obj.name = name
        company_obj.code = code
        company_obj.save()
        return HttpResponse("<h1>操作成功，刷新页面即可。</h1>")

def delete_company(request,id):
    if request.method == "GET":
        company_obj = company.objects.get(id=id)
        company_obj.delete()
        return redirect(to="/data/company_show/")

def department_show(request):
    if request.method == "GET":
        department_obj = department.objects.all()
        return render(request,"department_show.html",paginator(request,department_obj))

def search_department(request):
    if request.method == "GET":
        department_name = request.GET.get("search1")
        department_obj = department.objects.filter(name__icontains=department_name)
    if request.method == "POST":
        department_code = request.POST.get("search2")
        department_obj = department.objects.filter(code__icontains=department_code)
    return render(request,"department_show.html",paginator(request,department_obj))

def insert_department(request):
    if request.method == "GET":
        company_obj = company.objects.all()
        return render(request,"insert_department.html",locals())
    if request.method == "POST":
        company_code = request.POST.get("company")
        department_name = request.POST.get("department_name")
        department_code = request.POST.get("department_code")
        if department_name == "" or department_code == "":
            return HttpResponse("请填写部门与编码。")
        company_obj = company.objects.get(code=company_code)
        department_name_obj = department.objects.filter(company=company_obj,name=department_name)
        if department_name_obj:
            return HttpResponse("该部门已存在，请勿重复添加。")
        department_code_obj = department.objects.filter(company=company_obj,code=department_code)
        if department_code_obj:
            return HttpResponse("该部门编码可能与其它部门编码冲突，尝试换个编码命名。")
        department.objects.create(name=department_name,code=department_code,company=company_obj)
        return HttpResponse("<h1>操作成功，刷新页面即可。</h1>")

def update_department(request,id):
    department_obj = department.objects.get(id=id)
    if request.method == "GET":
        company_obj = company.objects.all()
        return render(request,"updateDepartment.html",locals())
    if request.method == "POST":
        company_code = request.POST.get("company")
        department_name = request.POST.get("department_name")
        department_code = request.POST.get("department_code")
        if department_name == "" or department_code == "":
            return HttpResponse("<h1>请填写部门与编码。<h1>")
        company_obj = company.objects.get(code=company_code)
        if department_name == department_obj.name:
            pass
        else:
            department_name_obj = department.objects.filter(company=company_obj,name=department_name)
            if department_name_obj:
                return HttpResponse("<h1>该部门已存在，请勿重复添加。</h1>")
        if department_code == department_obj.code:
            pass
        else:
            department_code_obj = department.objects.filter(company=company_obj,code=department_code)
            if department_code_obj:
                print(department_code_obj[0].code,department_code)
                return HttpResponse("<h1>该部门编码可能与其它部门编码冲突，尝试换个编码命名。</h1>")
        department_obj.name = department_name
        department_obj.code = department_code
        department_obj.save()
        return HttpResponse("<h1>操作成功，刷新页面即可。</h1>")


def delete_department(request,id):
    if request.method == "GET":
        department_obj = department.objects.get(id=id)
        department_obj.delete()
        return redirect(to="/data/department_show/")
