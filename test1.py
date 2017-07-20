import requests
import json
import unittest
import re
import xlrd
import logging
import os


def run_testcase():
    testCase = xlrd.open_workbook(r'C:/Users/yunji003/Desktop/pythonscript/testCase2.xlsx')
    table = testCase.sheet_by_index(0)
    session = get_cookie()
    sum=0
    for i in range(0, table.nrows):
        module = table.cell(i, 0).value.replace('\n', '').replace('\r', '')
        case_status = table.cell(i, 1).value.replace('\n', '').replace('\r', '')
        method = table.cell(i, 2).value.replace('\n', '').replace('\r', '')
        APIname = table.cell(i, 3).value.replace('\n', '').replace('\r', '')
        data = table.cell(i, 4).value.replace('\n', '').replace('\r', '')
        expected_response = table.cell(i, 5).value.replace('\n', '').replace('\r', '')
        result2=expected_response.encode('utf8')
        result2=json.loads(result2)
        response = interface_test(module, case_status, method, APIname, data, expected_response, session)
        response = response.json()
        result1=response
        
        if cmp(result1,result2)!=0:
            sum=sum+1
    return sum





def interface_test(module, case_status, method, APIname, data, expected_response, session):
    head = {
        'Cookie': 'modules=132; modulesR=132; accountId=1; parentUserId=503; groupId=null; userName=aW50ZXJuYWxhZG1pbkBmb3N1bi5jb20=; name=aW50ZXJuYWxhZG1pbg==; userId=503; appId=1; session=' + session}

    test_url = 'http://10.151.2.100:3003' + APIname

    if method == 'GET':
        response = requests.get(test_url, params=data, headers=head)
        return response
    elif method=='POST':
        data=data.encode('utf8')
        print type(data)
        data=json.dumps(data)
        print type(data)
        response = requests.post(test_url,json=data,headers=head)
        return response


def get_cookie():
    user_url = 'http://10.151.2.100:3003/dmp/loginTest'
    user_email = 'internaladmin@fosun.com'
    user_pwd = 'e10adc3949ba59abbe56e057f20f883e'

    data = {"username": user_email,
            "password": user_pwd}
    req = requests.get(user_url, params=data)

    cookie = req.json()
    cookie = cookie.get('data')
    return cookie.get('SESSION')


if __name__ == '__main__':
    print run_testcase()