#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys,os
from PyQt5.QtCore import QObject,pyqtSignal,pyqtSlot,QUrl,QCoreApplication  #,QTimer Qt,QThread,QBasicTimer,QUrl,QCoreApplication,QCoreApplication
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication,QMainWindow,QMessageBox  #, QMessageBox,QToolTip,QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView   #QWebEnginePage
from PyQt5.QtGui import QFont,QIcon
from PyQt5.QtWebChannel import QWebChannel
from time import sleep
import pget
from plogger import log_message,homepath,filepath,designpath
# import random
# import multiprocessing
# from information import inforapp
import myftp
from myftp import myFtp
# from closeapp import closeapp
from myftp import rate
from tokenpy import tokenfile,tokenmade


global interactionflag
interactionflag = 0

global networkflag
networkflag = 0

global parameter
parameter = 0


global argument
argument = 1

global restartflag
restartflag = 0

global loginflag
loginflag = 0

global LOCK
LOCK = 1

global startflag
startflag = 0

from threading import Thread
from threadpoolpy import ThreadPool

pool = ThreadPool(5)

import re

class CallHandler(QObject):

    def __init__(self,window):
        super().__init__()
        self.res = 0
        self.window = window

    @pyqtSlot(str)
    def myHello(self,arg1):
        global interactionflag
        global parameter
        global startflag
        interactionflag = 1
        startflag = 1
        parameter = arg1
        # print('call received')
        # print("winno")
        # print(arg1)
        argument = int(sys.argv[1])
        print('argument-myHello',argument)

        if argument == 0 or argument == 5:
            pool.run(func=self.window.uploadhome, args=())
        elif argument == 1 or argument == 6:
            pool.run(func=self.window.uploadfile, args=())
        elif argument == 2 or argument == 7:
            pool.run(func=self.window.uploaddesign, args=())

        pool.run(func=self.window.updateview, args=())


    # @pyqtSlot(str)
    # def mylogin(self,arg1):
    #     global loginflag
    #     global parameter
    #     loginflag = 1
    #     parameter = arg1
    #     print(arg1)


class MyWind(QMainWindow):
    global argument
    argument = int(sys.argv[1])
    # argument = 2

    ASignal = pyqtSignal(int,int,int)
    BSignal = pyqtSignal(float)
    CSignal = pyqtSignal(str)
    DSignal = pyqtSignal(str)
    # ESignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        # print("*args, **kwargs:",args, kwargs)
        self.setWindowTitle('庭好的')
        # self.setGeometry(100, 100, 800, 800)
        self.resize(900, 600)
        # self.setWindowIcon(QIcon('icons/logo.png'))
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.style = """ 
                 QPushButton{background-color:grey;color:white;} 
                #window{ background:blue}
                #test{ background-color:black;color:white; }
            """
        self.setStyleSheet(self.style + "#window{background:%s}")
        self.setFont(QFont('微软雅黑', 12))
        self.show()

        self.ftpstartflag = 0
        self.ftpcompleteflag = 0
        self.argv = argument




        self.browser = QWebEngineView()
        self.browser.urlChanged.connect(self.savetoken)

        # 添加浏览器到窗口中
        self.setCentralWidget(self.browser)
        # self.closeapp = closeapp()
        self.ASignal.connect(self.setmessage)
        self.BSignal.connect(self.setstatusFloat)
        self.CSignal.connect(self.setstatus)
        self.DSignal.connect(self.postmessage)
        # self.ESignal.connect(self.pbarshow)


        self.statusBar().showMessage(" ")



    def savetoken(self,q):

        #保存token
        print('url:', q.toString())
        try:
            res = re.findall(r"token=\$\[\#+(.+)\]\$", q.toString())
            if res:
                token = res[0]
                try:
                    # print('tokenfile',tokenfile)
                    f = open(tokenfile, 'w+')
                    f.write(token)

                finally:
                    f.close()
        except:
            # print("err",tokenfile)
            pass

    def closeEvent(self, QCloseEvent):
        global startflag
        global LOCK
        # print('self.ftpcompleteflag', self.ftpcompleteflag)
        # print('startflag', startflag)
        # print(startflag == 1 and self.ftpcompleteflag != 3 and self.ftpcompleteflag != 1 and self.ftpcompleteflag != 2)

        if startflag == 1 and self.ftpcompleteflag != 3 and self.ftpcompleteflag != 1 and self.ftpcompleteflag != 2 and self.ftpcompleteflag != 10:
            # reply = QMessageBox.question(self, '提醒', '上传未完成，确定要退出吗?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            # if reply == QMessageBox.Yes:
            #     LOCK = 0
            #     pool.terminate()
            #     QCloseEvent.accept()  # 接受关闭事件
            #
            # else:
            #     QCloseEvent.ignore()  # 忽略关闭事件
            reply = QMessageBox.question(self, '提醒', '上传未完成，请继续等待！',  QMessageBox.Ok, QMessageBox.Ok)
            QCloseEvent.ignore()  # 忽略关闭事件


        else:
            LOCK = 0
            pool.terminate()
            QCloseEvent.accept()
        # QCoreApplication.instance().quit()
        pass


    def postmessage(self,arg1):
        global LOCK
        global startflag
        reply = QMessageBox.information(self,  # 使用infomation信息框
                                        "上传结果",
                                        arg1,
                                        QMessageBox.Ok)

        if reply == QMessageBox.Ok:

            LOCK = 0
            self.close()
        pass

    def setmessage(self,num,s,type):
        textlist = ["户型上传失败!", "方案上传失败!", "文件上传失败!", "户型上传成功!", " 方案上传成功!", "渲染提交成功，请等待短信通知!"]
        text = ["户型文件不存在","方案文件不存在","渲染文件不存在,请确保在3D环境下渲染"]

        # if s == 1:
        #     self.closeapp.show()
        #     self.closeapp.settext(str(textlist[num]))
        #
        # elif int(rate[0])==1 and s == 2:
        #     self.closeapp.show()
        #     self.closeapp.settext("请求失败!")
        #
        # elif int(rate[0])==1 and s == 3:
        #     self.closeapp.show()
        #     self.closeapp.settext(str(textlist[num+3]))
        #     self.ftpcompleteflag = 0
        if type == 1:
            self.DSignal.emit(str(text[num]))

        elif type == 0:
            if s == 1:
                self.DSignal.emit(str(textlist[num]))

            elif int(rate[0])==1 and s == 2:
                self.DSignal.emit("请求失败!")

            elif int(rate[0])==1 and s == 3:
                self.DSignal.emit(str(textlist[num+3]))
                self.ftpcompleteflag = 10



    def setstatusFloat(self,value):
        self.msg = "%.0f%%" % (value * 100)
        self.statusBar().showMessage("上传进度：" + self.msg)

    def setstatus(self, value):
        self.statusBar().showMessage(value)


    def updateview(self):
        global rate
        global restartflag
        sleep(0.7)

        while LOCK:
            print("thread1:")
            if self.ftpstartflag == 1:
                if int(rate[3]) == 1:
                    self.CSignal.emit("正在打包压缩")
                    sleep(1.51)
                else:
                    self.BSignal.emit(rate[0])
                    # sleep(0.53)

                if int(rate[0])==1:
                    # print('thread1 break')

                    return

                if self.ftpcompleteflag == 1 or self.ftpcompleteflag == 2:
                    print('thread1 break')
                    return
            else:
                self.CSignal.emit(rate[0])

            # if(self.ftpstartflag == 0):
            #     sleep(1.1)

    def uploaddesign(self):
        global parameter
        global interactionflag
        global rate
        global networkflag
        global restartflag
        # sleep(3)
        self.ftpcompleteflag = 0
        rate[0] = 0.0
        while LOCK:
            print("thread2")
            # sleep(0.6)

            if (interactionflag):
                print("thread2")
                interactionflag = 0
                log_message(designpath, "-------------start-------------", "" + '\n')
                try:
                    self.ftpstartflag = 1
                    log_message(designpath, "FTP上传设计文件和纹理文件开始", "" + '\n')
                    myftp.ftpuploadess(parameter)
                    # log_message(designpath, "FTP上传纹理文件开始", "" + '\n')
                    # myftp.ftpuploadtexture()
                    print("rate[0]",rate[0])
                    self.BSignal.emit(rate[0])
                except Exception as err:
                    print(err)

                    log_message(designpath, "FTP上传失败：", str(err) + '\n')
                    self.ftpcompleteflag = 1
                    if "file not exists" in str(err):
                        self.ASignal.emit(2, self.ftpcompleteflag, 1)
                    else:
                        self.ASignal.emit(2, self.ftpcompleteflag,0)
                    print("thread2 break")
                    return
                log_message(designpath, "FTP上传成功", "" + '\n')

                try:
                    if self.argv < 5:
                        log_message(designpath, "开始请求地址(get):", "http://h5.thd99.com:9999/farm/win.html?winNo="+str(parameter) + '\n')
                    else:
                        log_message(designpath, "开始请求地址(get):",
                                    "http://h5.91thd.com:80/farm/win.html?winNo=" + str(parameter) + '\n')
                    b = str(int(parameter))
                    print(b)
                    pget.connethost(b,self.argv)
                except Exception as err:
                    print(err)
                    self.ftpcompleteflag = 2
                    self.ASignal.emit(2, self.ftpcompleteflag,0)
                    print("thread2 break")
                    return

                self.ftpcompleteflag = 3
                self.ASignal.emit(2,self.ftpcompleteflag,0)
                print("thread2 break")
                return

    def uploadfile(self):
        global parameter
        global interactionflag
        global rate
        global networkflag

        # sleep(3)
        self.ftpcompleteflag = 0
        rate[0] = 0.0
        while LOCK:
            print("thread2")
            # print("parameter type",type(parameter))

            # sleep(0.5)


            if (interactionflag):
                interactionflag = 0
                log_message(filepath, "-------------start-------------", "" + '\n')
                try:
                    log_message(filepath, "FTP上传开始", "" + '\n')
                    self.ftpstartflag = 1
                    myftp.ftpuploadfile(parameter)
                    self.BSignal.emit(rate[0])
                except Exception as err:

                    log_message(filepath, "FTP上传失败：", str(err) + '\n')
                    self.ftpcompleteflag = 1
                    if "file not exists" in str(err):
                        self.ASignal.emit(1, self.ftpcompleteflag,1)
                    else:
                        self.ASignal.emit(1, self.ftpcompleteflag,0)
                    return
                log_message(filepath, "FTP上传成功", "" + '\n')

                try:
                    if self.argv < 5:
                        log_message(filepath, "开始请求地址(get):", "http://h5.thd99.com:9999/win/win.html?winno="+str(parameter) + '\n')
                    else:
                        log_message(filepath, "开始请求地址(get):",
                                    "http://h5.91thd.com:80/win/win.html?winno=" + str(parameter) + '\n')
                    b = str(int(parameter))
                    # print(b)
                    pget.connethost(b,self.argv)
                except Exception as err:
                    # print(err)
                    self.ftpcompleteflag = 2
                    self.ASignal.emit(1, self.ftpcompleteflag,0)
                    return
                self.ftpcompleteflag = 3
                print("sucuss")
                self.ASignal.emit(1, self.ftpcompleteflag,0)
                return

    def uploadhome(self):
        global parameter
        global interactionflag
        global rate
        global networkflag
        rate[0] = 0.0
        # sleep(3)
        self.ftpcompleteflag = 0

        while LOCK:
            print("thread2")
            # print("parameter:",(parameter))
            # print("interactionflag:",(interactionflag))
            # sleep(0.5)


            if (interactionflag):
                interactionflag = 0
                log_message(homepath, "-------------start-------------", "" + '\n')
                try:
                    log_message(homepath, "FTP上传开始", "" + '\n')
                    self.ftpstartflag = 1
                    myftp.ftpuploadhome(parameter)
                    self.BSignal.emit(rate[0])
                except Exception as err:

                    log_message(homepath, "FTP上传失败：", str(err) + '\n')
                    self.ftpcompleteflag = 1
                    if "file not exists" in str(err):
                        self.ASignal.emit(0, self.ftpcompleteflag,1)
                    else:
                        self.ASignal.emit(0, self.ftpcompleteflag,0)
                    return
                log_message(homepath, "FTP上传成功", "" + '\n')

                try:
                    if self.argv<5:
                        log_message(homepath, "开始请求地址(get):", "http://h5.thd99.com:9999/unit/back.html?unit_no=" + str(parameter) + '\n')
                    else:
                        log_message(homepath, "开始请求地址(get):",
                                    "http://h5.91thd.com:80/unit/back.html?unit_no=" + str(parameter) + '\n')
                    b = str(int(parameter))
                    # print(b)
                    pget.connethost(b,self.argv)
                except Exception as err:
                    # print(err)
                    self.ftpcompleteflag = 2
                    self.ASignal.emit(0, self.ftpcompleteflag,0)
                    return
                self.ftpcompleteflag = 3
                self.ASignal.emit(0, self.ftpcompleteflag,0)
                return


if __name__ == '__main__':

        num = int(sys.argv[1])
        # print("start sysargu:",sys.argv[2])
        # num = 2
        print("mainloop num", num)
        urllist=["http://h5.thd99.com:9999/unit?siid=100","http://h5.thd99.com:9999/win?siid=100","http://h5.thd99.com:9999/farm?siid=100"]

        if num > 4:
            num = num-5
            print("num", num)
            urllist = ["http://h5.91thd.com/unit?siid=100","http://h5.91thd.com/win?siid=100","http://h5.91thd.com/farm?siid=100"]

        # url_string = ["http://1.wery.applinzi.com/index.html","D:/myproject/pythonproject/upload20171225/test.html","http://h5.thd99.com:9999/farm?siid=100"]

        if os.path.isfile(tokenfile) == True:
            # urllist = ["http://h5.thd99.com:9999/unit", "http://h5.thd99.com:9999/win","http://h5.thd99.com:9999/farm"]  #url = urllist[num]+'?token='+token
            try:
                token = tokenmade()
                url = urllist[num]+'&token='+token
                print('url',url)
            except:
                url = urllist[num]
        else:
            url = urllist[num]

        app = QApplication(sys.argv)

        window=MyWind()
        channel = QWebChannel()
        handler = CallHandler(window)
        # re = handler.myHello(2017101908712215730)
        channel.registerObject('pyjs', handler)
        window.browser.page().setWebChannel(channel)
        # url = 'http://h5.thd99.com:9999/farm?siid=100?token=QytoSUtJampiTDFSNHB0L3R5UllVRmc2aFhQaGVET3gzSTZRK3BUaFpOT0lZd0FFcEs2bjRvL1drMVg4d2YvZ2E5c0ZKQlNudUNHekhJaDNqU2FpUkFQd1dERlVLcEJaTk5KcUcwS0RyVTF2ZjV5MTJLMStOcm5ZVElxUXY1Q0lRMmk4Ym9lVXI2TDF5VmZTZ1RjN3hMaEJWRWlzUWF1TmMzQmdRS0VuNzk4PQ=='
        window.browser.load(QUrl(url))
        # window.uploaddesign()
        window.browser.show()
        print("final")
        window.show()
        app.exec_()

