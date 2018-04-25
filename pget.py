#!/usr/bin/env python
#coding=utf8

import http.client
import datetime
import time
from time import sleep
import json
from plogger import log_message,path
import sys

httpClient = None

def connethost(winno,n):
    try:
        print("n=",n)
        if n==0:
            httpClient = http.client.HTTPConnection('h5.thd99.com', 9999, timeout=30)
            para = '/unit/back.html?unit_no=' + str(winno)
        elif n==1:
            httpClient = http.client.HTTPConnection('h5.thd99.com', 9999, timeout=30)
            para = '/win/win.html?winno=' + str(winno)
        elif n==2:
            httpClient = http.client.HTTPConnection('h5.thd99.com', 9999, timeout=30)
            para = '/farm/win.html?winNo='+str(winno)
        elif n==5:
            httpClient = http.client.HTTPConnection('h5.91thd.com', 80, timeout=30)
            para = '/unit/back.html?unit_no=' + str(winno)
            print("n==5")
        elif n==6:
            httpClient = http.client.HTTPConnection('h5.91thd.com', 80, timeout=30)
            para = '/win/win.html?winno=' + str(winno)
        elif n==7:
            httpClient = http.client.HTTPConnection('h5.91thd.com', 80, timeout=30)
            para = '/farm/win.html?winNo=' + str(winno)

        httpClient.request('GET', para)

        #response是HTTPResponse对象
        response = httpClient.getresponse()
        re = response.read()
        print(response.status)
        print(response.reason)
        print(re)
        resp = json.loads(re)
        if n < 5:
            log_message(path[n], "请求返回：", str(resp['msg']) + '\n')
        else:
            log_message(path[n-5], "请求返回：", str(resp['msg']) + '\n')

        if(response.status == 200 and resp['state'] ==1100 and resp['msg']=="成功"):
            print(resp['state'])
            print(resp['msg'])

    except Exception as err:
        print(err)
        raise IOError("request fail")
    finally:
        if httpClient:
            httpClient.close()



if __name__ == '__main__':
    # winno = 201710250519231003291007
    winno = 201711030519231005291007
    #           2017110305192310052
    print(winno)
    connethost(winno,0)

    # while True:
    # try:
    #     connethost()
    # except Exception as err:
    #     print(err)
    # print("456")

        # sleep(100)