import re
from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.csrf import csrf_exempt
from userControl.models import *
from mainControl.views import paginator,get_access_token,get_user_info,get_userID
from django.core.cache import cache
# Create your views here.



# 登录
@csrf_exempt
def login(request):
    if request.method == "GET":
        return render(request,"login.html")
    if request.method == "POST":
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        print(phone,password)
        try:
            user_obj = userInfo.objects.get(phone=phone)
            print(user_obj)
            if user_obj.password == password:
                request.session["user_id"] = user_obj.id
                return redirect(to='/main/index/')
        except Exception as e:
            print(e)
            message = "账号或密码错误"
            return render(request,"login.html",locals())

# 账号注册
def register(request):
    if request.method == "GET":
        return render(request,"register.html")
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        phone =request.POST.get("phone")
        if username and password1 and password2 and phone:
            if password1 != password2:
                message = "两次密码输入不一样"
                return render(request,"register.html",locals())
            result = re.match(r"^1[3456789]\d{9}$",phone)
            print(result,phone)
            if result is None:
                message = "手机号格式不正确"
                return render(request,"register.html",locals())
            userInfo.objects.create(username=username,password=password1,phone=phone)
            message = "注册完成"
            return render(request,"login.html",locals())
        message = "所有必填项不可为空"
        return render(request,"register.html",locals())

# 用户信息展示
def usershow(request):
    if request.method == "GET":
        user_obj = userInfo.objects.all()
        return render(request,"userInfo_show.html",paginator(request,user_obj))
# 新增用户
def insertUser(request):
    if request.method == "GET":
        company_obj = company.objects.all()
        return render(request,"insertUser.html",locals())
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        real_name = request.POST.get("real_name")
        phone = request.POST.get("phone")
        companys = request.POST.get("company")
        departments = request.POST.get("department")
        comment = request.POST.get("comment")
        userInfo.objects.create(username=username,password=password,real_name=real_name,phone=phone,company=companys,department=departments,comment=comment)
        return HttpResponse("<h1>添加成功，刷新页面即可</h1>")
    
# 信息查询（根据用户名查询）
@csrf_exempt
def search_user(request):
    if request.method == "GET":
        search_name = request.GET.get("search1")
        user_obj = userInfo.objects.filter(username__icontains=search_name)
    if request.method == "POST":
        search_name = request.POST.get("search2")
        print(search_name)
        user_obj = userInfo.objects.filter(real_name__icontains=search_name)
    return render(request,"userInfo_show.html",paginator(request,user_obj))

# 个人信息修改
def update(request,id):
    id = int(id)
    user_obj = userInfo.objects.get(id=id)
    company_id = company.objects.get(name=user_obj.company)
    company_obj = company.objects.all()
    department_obj = department.objects.filter(company_id=company_id)
    if request.method == "GET":
        return render(request,"updateUser.html",locals())

    if request.method == "POST":
        username = request.POST.get("username")
        real_name = request.POST.get("real_name")
        phone =  request.POST.get("phone")
        comment = request.POST.get("comment")
        updatecompany = request.POST.get("company")
        updatedepartment = request.POST.get("department")
        if username == "" or real_name == "" or phone == "" or updatecompany == "" or updatedepartment == "":
            return HttpResponse("<h1>前五项字段不可为空!</h1>")
        result = re.match(r"^1[3456789]\d{9}$",phone)
        if result is None:
            return HttpResponse("<h1>手机号格式不正确</h1>")
        user_obj.username = username
        user_obj.real_name = real_name
        user_obj.phone = phone
        user_obj.company = updatecompany
        user_obj.department = updatedepartment
        user_obj.comment = comment
        user_obj.save()
        return HttpResponse("<h1>修改完成！刷新页面即可。</h1>")

# 修改个人密码
def uppassword(request,id):
    id = int(id)
    if request.method == "GET":
        return render(request,"updatePassword.html",locals())
    if request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        user_obj = userInfo.objects.get(id=id)
        user_password = user_obj.password
        if password1 != user_password:
            return HttpResponse("<h1>密码错误，请重新输入。</h1>")
        user_obj.password = password2
        user_obj.save()
        return HttpResponse("<h1>修改完成！刷新页面即可。</h1>")

def dingdingEnter(request):
    if request.method == "GET":
        return render(request,"verifyIdentity.html")

def verifyIdentity(request):
    if request.method == "GET":
        code =  request.GET.get("code")
        if code:
            access_token = cache.get("access_token")
            try:
                user_id,scan_name = get_userID(request,access_token,code)
            except:
                access_token = get_access_token(request)
                user_id,scan_name = get_userID(request,access_token,code)

            if user_id: #获取扫码人的个人详情
                scan_name,phone = get_user_info(request,access_token,user_id)
            try:
                user_obj = userInfo.objects.get(real_name=scan_name,phone=phone)
                if user_obj:
                    request.session['company'] = user_obj.company
                    return redirect(to=f"/main/index/?login_company={user_obj.company}")
            except:
                return HttpResponse(f"<h1>您为非管理员！若要进入可联系资产管理管理员</h1>")
        return HttpResponse("<h1>该接口为钉钉入口。</h1>")
