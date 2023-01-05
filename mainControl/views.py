from django.shortcuts import render,HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger,InvalidPage
import requests
from dingtalk import SecretClient
from django.core.cache import cache
from Resource.settings import *

# Create your views here.

# 封装分页器,避免代码太多重复
def paginator(request,index_list):
    print("使用了分页器")
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
    return {"lenlist":lenlist,"pageRange":pageRange,"index_list":obj_list}

# 获取企业内部应用的access_tokenpython 获取钉钉用户userid
def get_access_token(request):
    if request.method == "GET":
        client = SecretClient(APPKEY, APPSECRET)  #新 access_token 获取方式
        access_token = client.access_token
        cache.set("access_token",access_token,60*60*2)
        print("token为：",access_token)
        return access_token

# 获取用户id
def get_userID(request,access_token,code):
    url = "https://oapi.dingtalk.com/topapi/v2/user/getuserinfo"
    params = {"access_token":access_token,"code":code}
    data = requests.get(url,params=params)
    print("返回user响应",data.json())
    userID = data.json().get("result").get("userid")
    scan_name = data.json().get('result').get('name')
    return userID,scan_name

# 获取用户详细信息
def get_user_info(request,access_token,userID):
    url = "https://oapi.dingtalk.com/topapi/v2/user/get"
    params = {"access_token":access_token,"userid":userID}
    data = requests.get(url,params=params)
    scan_name = data.json().get('result').get('name')
    phone = data.json().get('result').get('mobile')
    print("扫码人详情：",scan_name,phone)
    return scan_name,phone


def index(request):
    if request.method == "GET":
        login_company = request.GET.get("login_company")
        return render(request,"index.html",locals())

def index_data(request):
    if request.method == "GET":
        return render(request,"index_data.html")