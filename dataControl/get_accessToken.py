<<<<<<< HEAD
# -*- coding: utf-8 -*-
# access_token = "532a7c5760e3389b837555f064fa90af"
# import dingtalk,requests,json
# url = "https://oapi.dingtalk.com/gettoken?appkey=dingex3ufgx6u2hmv0k7&appsecret=hOkKqbMcVOApokfNZw7ER6Mb9lt5nIxSRU26TwjAp-msOzcu9u_Id-sVC7XHe32P"
# response = requests.get(url)
# code_dict = json.loads(response.content)
# print(code_dict)

import json
import pymysql
from dingtalk import SecretClient, AppKeyClient

##定义变量
E_AppKey = "dingex3ufgx6u2hmv0k7"
E_AppSecret ="hOkKqbMcVOApokfNZw7ER6Mb9lt5nIxSRU26TwjAp-msOzcu9u_Id-sVC7XHe32P"

##连接
client = SecretClient(E_AppKey, E_AppSecret)  #新 access_token 获取方式
print(client)

def getdepartments(departmentid):
    '''
    :param departmentid: 部门id，默认是1，即是获取所有的部门
    :return:departmentid下所有部门的id，namehe parentid
    '''
    result = {}
    departmentid =[]
    responses = client.department.list(departmentid, fetch_child=True)

    for response in responses:
        result['id']= response.get('id')
        result['name']= response.get('name')
        result['parentid']= response.get('parentid')
        
        if result['parentid'] == None:
            result['parentid'] = 0
        departmentid.append(response.get('id'))
    print(result)
    # print(departmentid)
    return departmentid


def getDepartmemtInfo(departmentid):
    '''
    :param departmentid:部门id
    :return: 部门信息
    '''
    responses = client.department.get(departmentid)
    #print(responses)
    return responses


def getuser(departmentid):
    '''
    :param departmentid: 获取部门下的用户（不包括子部门）
    :return: 用户信息
    '''
    res = {}
    userid =[]
    responses = client.user.list(departmentid)
    #print(responses)
    a = responses.get('userlist')
    
   
    for response in a:
        #print(response.get('department'))
        res['department']= response.get('department')
        res['userid']=response.get('userid')
        res['name']=response.get('name')
        res['mobile']=response.get('mobile')
        res['active']=response.get('active')
        res['unionid']=response.get('unionid')
        print(res)
        userid.append(response.get('userid')) #用户id列表
    #print(userid)
    return userid



def getEmployeeUserInfo(userid):
    '''
    :param userid:用户钉钉的userid 
    :return: 用户的花名册（详细信息）
    '''
    res = client.employeerm.get(userid)
    print(res)
    return res


if __name__ == '__main__':
    # departmentid = getdepartments(1)
    useridlist =[]

    # #用户表数据循环
    # for x in departmentid:
    userid = getuser("721734945")
    useridlist.extend(userid)
    print("==================")
    print(useridlist)
=======
for i in range(3):
    if i == 1:
        continue
    print(i)
>>>>>>> cd082f6 (second)
