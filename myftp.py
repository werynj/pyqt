# -*- coding:utf-8 -*-

from ctypes import *
import os
import sys
import ftplib
# import shutil
import time
import random
import shutil
global rate
rate = [0.0,0,0,0,0]
import zipfile

#压缩文件或文件夹为zip
def zip_dir(srcPath,dstname):
    zipHandle=zipfile.ZipFile(dstname,'w',zipfile.ZIP_DEFLATED)

    for dirpath,dirs,files in os.walk(srcPath):
        for filename in files:
            zipHandle.write(os.path.join(dirpath,filename)) #必须拼接完整文件名，这样保持目录层级
            print(filename+" zip succeeded")

    zipHandle.close

def zip_file(srcname,dstname):
    global rate
    zipHandle=zipfile.ZipFile(dstname,'w',zipfile.ZIP_DEFLATED)
    zipHandle.write(srcname) #必须拼接完整文件名，这样保持目录层级
    print(srcname+" zip succeeded")
    zipHandle.close
    rate[2] = 1

#解压zip文件
def unzip_dir(srcname,dstPath):
    zipHandle=zipfile.ZipFile(srcname,"r")
    for filename in zipHandle.namelist():
        print(filename)
    zipHandle.extractall(dstPath) #解压到指定目录

    zipHandle.close()


class myFtp:
    ftp = ftplib.FTP()
    bIsDir = False
    path = ""
    global rate


    def __init__(self, host, port):
        # self.ftp.set_debuglevel(2) #打开调试级别2，显示详细信息
        # self.ftp.set_pasv(0)      #0主动模式 1 #被动模式
        self.ftp.connect(host, port)



    def Login(self, user, passwd):
        self.ftp.login(user, passwd)
        # print(self.ftp.welcome)


    def DownLoadFile(self, LocalFile, RemoteFile):
        print(LocalFile)
        print(RemoteFile)
        file_handler = open(LocalFile, 'wb')
        self.ftp.retrbinary("RETR %s" % (RemoteFile), file_handler.write)
        file_handler.close()
        return True

    def UpLoadFile(self, LocalFile, RemoteFile):
        # print("err10")
        if os.path.isfile(LocalFile) == False:
            raise IOError("file not exists")
        fsize = os.stat(LocalFile).st_size  # 获取本地文件的大小
        file_handler = open(LocalFile, "rb")
        self.ftp.storbinary('STOR %s' % RemoteFile, file_handler, fsize)
        file_handler.close()
        return True

    def UpLoadFiles(self, LocalFile, RemoteFile,flag):
        # print("err10")
        if os.path.isfile(LocalFile) == False:
            raise IOError("file not exists")

        fsize = os.stat(LocalFile).st_size  # 获取本地文件的大小
        # print("fsize",fsize,type(fsize))
        if fsize == 0:
            raise IOError("file not exists")

        if fsize > 16000000:
            size = int(fsize/2) + 1
        else:
            size = fsize
        # print(size)
        file_handler = open(LocalFile, "rb")
        self.ftp.storbinarys('STOR %s' % RemoteFile, file_handler,rate, size, None, 0, fsize, flag)
        file_handler.close()
        return True


    def UpLoadFileTree(self, LocalDir, RemoteDir):
        if os.path.isdir(LocalDir) == False:
            raise IOError("file not exists")

        LocalDir=os.path.abspath(LocalDir)
        print("LocalDir:", LocalDir)

        LocalNames = os.listdir(LocalDir)
        print("list:", LocalNames)
        print(len(LocalNames))

        print(RemoteDir)
        try:
            self.ftp.cwd(RemoteDir)
        except ftplib.error_perm:
            try:
                self.ftp.mkd(RemoteDir)

            except ftplib.error_perm:
                print('U have no authority to make dir')
                self.ftp.cwd(RemoteDir)
        i = 0
        for Local in LocalNames:
            i = i+1
            # print(rate[0])
            rate[0] = i/len(LocalNames)

            src = os.path.join(LocalDir, Local)
            print("src:"+src)
            print("local:"+Local)
            if os.path.isdir(src):
                self.UpLoadFileTree(src, Local)
            else:
                self.UpLoadFile(src, Local)

        self.ftp.cwd("..")
        return


    def UpLoadtexture(self, LocalDir, RemoteDir,texturefile):

        if os.path.isdir(LocalDir) == False:
            raise IOError("file not exists")

        LocalNames = os.listdir(LocalDir)
        print("LocalDir:"+LocalDir)
        print("list:", LocalNames)
        # print(len(LocalNames))
        print(RemoteDir)
        try:
            self.ftp.cwd(RemoteDir)
        except ftplib.error_perm:
            try:
                self.ftp.mkd(RemoteDir)

            except ftplib.error_perm:
                print('U have no authority to make dir')
                self.ftp.cwd(RemoteDir)

        # print("texturefile:"+texturefile)

        try:
            file = open(texturefile, 'a+')
        finally:
            if file:
                file.close()


        lines = []

        # file = open(texturefile)
        for line in open(texturefile):

            line = line.strip('\n')
            lines.append(line)

        print("lines:"+str(lines))

        file = open(texturefile, 'a+')
        # print("debug01")
        k = 0.0
        print("rate:")
        print(rate[0])
        i = 0
        length = len(LocalNames)
        for Local in LocalNames:

            exitflag = 0
            i = i+1
            k = float(float(i)/float(length))*0.75+0.25
            rate[0] = k
            # print("rate:",rate[0])
            # print("debug03")
            for line in lines:
                if Local == line:
                    exitflag = 1
                    # print("exist")
                    break
            if exitflag == 0:
                print(Local)
                file.write(Local + '\n')
                # print("not exist")
                # exitflag = 0

                src = os.path.join(LocalDir, Local)
                # print("srcdebug:"+src)
                # print("local:"+Local)
                if os.path.isdir(src):
                    self.UpLoadFileTree(src, Local)

                else:
                    self.UpLoadFile(src, Local)
                # time.sleep(0.1)

        self.ftp.cwd("..")
        if file:
            file.close()
        return

    def DownLoadFileTree(self, LocalDir, RemoteDir):
        print("remoteDir:", RemoteDir)
        if os.path.isdir(LocalDir) == False:
            os.makedirs(LocalDir)
        self.ftp.cwd(RemoteDir)
        RemoteNames = self.ftp.nlst()
        print("RemoteNames", RemoteNames)
        print(self.ftp.nlst("/del1"))

        for file in RemoteNames:
            Local = os.path.join(LocalDir, file)
            print('Local '+str(Local))
            if self.isDir(file):
                self.DownLoadFileTree(Local, file)
            else:
                self.DownLoadFile(Local, file)
        self.ftp.cwd("..")
        return

    def DownLoadFileTreebk(self, LocalDir, RemoteDir):
        print("remoteDir:", RemoteDir)
        if os.path.isdir(LocalDir) == False:
            os.makedirs(LocalDir)
        self.ftp.cwd(RemoteDir)
        RemoteNames = self.ftp.nlst()
        print("RemoteNames", RemoteNames)
        print(self.ftp.nlst("/del1"))

        for file in RemoteNames:
            Local = os.path.join(LocalDir, file)
            print('Local '+str(Local))
            if self.isDir(file):
                self.DownLoadFileTreebk(Local, file)
            else:
                self.DownLoadFilebk(Local, file)
        self.ftp.cwd("..")
        return

    def show(self, list):
        result = list.lower().split(" ")
        if self.path in result and "<dir>" in result:
            self.bIsDir = True

    def isDir(self, path):
        self.bIsDir = False
        self.path = path
        # this ues callback function ,that will change bIsDir value
        self.ftp.retrlines('LIST', self.show)
        return self.bIsDir

    def close(self):
        self.ftp.quit()

def ftpupload(a):

    ftp = myFtp('192.168.0.74', 21)
    ftp.Login('zhf', '16696')

    romotefolder = 'uphome/' + str(a) + '/'
    print(romotefolder)

    # localfolder  = 'D:/Program Files (x86)/THD/Temp'
    localfolder = os.path.join(os.path.dirname(os.path.dirname(sys.argv[0])), "Temp")
    print("localfolder:"+localfolder)
    # try:
    #     ftp.UpLoadFileTree(localfolder, romotefolder)
    # except Exception as err:
    #     print(err)
    #     pass
    ftp.UpLoadFileTree(localfolder, romotefolder)
    ftp.close()
    # post 请求给平台
    print("ok!")

def ftpuploadhome(a):

    ftp = myFtp('h.thd99.com',2121)
    ftp.Login('elarauser', '123456')

    romotefolder = 'uphome/' + str(a) + '/'

    print(romotefolder)
    try:
        ftp.ftp.cwd(romotefolder)
    except ftplib.error_perm:
        try:
            ftp.ftp.mkd(romotefolder)

        except ftplib.error_perm:
            print('U have no authority to make dir')
        ftp.ftp.cwd(romotefolder)


    # localfolder  = 'D:/Program Files (x86)/THD/Temp'
    localfolder = os.path.join(os.path.dirname(os.path.dirname(sys.argv[0])), "Temp")


    print("localfolder:",os.path.dirname(os.path.dirname(sys.argv[0])))
    localname = os.path.join(localfolder, "home.jpg")
    romotename = "home.jpg"
    ftp.UpLoadFile(localname,romotename)
    rate[0]= 0.5
    localname = os.path.join(localfolder, "home.hom")
    romotename = "home.hom"
    ftp.UpLoadFile(localname,romotename)
    rate[0]= 1.0
    ftp.close()
    # post 请求给平台
    print("ok!")

def ftpuploadfile(a):

    ftp = myFtp('h.thd99.com',2121)
    ftp.Login('elarauser', '123456')

    print("debug01")
    romotefolder = 'upfile/' + str(a) + '/'
    print(romotefolder)

    try:
        ftp.ftp.cwd(romotefolder)
    except ftplib.error_perm:
        try:
            ftp.ftp.mkd(romotefolder)

        except ftplib.error_perm:
            print('U have no authority to make dir')
        ftp.ftp.cwd(romotefolder)

    # localfolder  = 'D:/Program Files (x86)/THD/Temp'
    # print("debug02")
    localfolder = os.path.join(os.path.dirname(os.path.dirname(sys.argv[0])), "Temp")
    # print("localfolder",localfolder)
    # print("debug021")
    localname = os.path.join(localfolder, "thd.dxf")
    # print("debug022")
    romotename = "thd.dxf"
    # print("debug023")
    ftp.UpLoadFiles(localname,romotename,0)

    localname = os.path.join(localfolder, "thd.hom")
    romotename = "thd.hom"
    ftp.UpLoadFiles(localname,romotename,1)
    localname = os.path.join(localfolder, "thd.jpg")
    romotename = "thd.jpg"
    ftp.UpLoadFiles(localname,romotename,2)
    print("debug03")
    localname = os.path.join(localfolder, "thd.txt")
    romotename = "thd.txt"
    ftp.UpLoadFile(localname,romotename)
    rate[0] = 1
    print("debug04")
    ftp.close()
    # post 请求给平台
    print("ok!")

def ftpuploadess(a):
    # dict['count'] = 138
    # ftp = myFtp('192.168.0.74', 21)
    # ftp.Login('zhf', '16696')
    ftp = myFtp('h.thd99.com',2121)
    ftp.Login('elarauser', '123456')

    # rootfolder =  os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(sys.argv[0]))))
    root = (os.path.dirname(os.path.dirname(sys.argv[0])))
    rootfolder = root[0] + ':/'
    print(rootfolder)
    essfile = os.path.join(rootfolder,'test.ess')
    print(essfile)

    if os.path.exists(essfile) == False:
        raise IOError("file not exists")

    # localfolder = (os.path.dirname(sys.argv[0]))
    localfolder = rootfolder
    filename = '%s.ess' % (a)
    localfile = os.path.join(rootfolder,filename)
    print('localfile:'+localfile)
    os.rename(essfile, localfile)

    # shutil.copyfile(essfile, localfile)
    zipfile = '%s.zip' % (a)
    localzipfile = os.path.join(rootfolder,zipfile)
    print('localzipfile:'+localzipfile)
    rate[3] = 1
    zip_file(localfile, localzipfile)
    rate[3] = 0

    romotefolder = '/input/'

    try:
        ftp.ftp.cwd(romotefolder)
    except ftplib.error_perm:
        try:
            ftp.ftp.mkd(romotefolder)

        except ftplib.error_perm:
            print('U have no authority to make dir')
        ftp.ftp.cwd(romotefolder)

    localzipfile = os.path.join(localfolder, zipfile)
    romotename = zipfile
    print("localzipfile:",localzipfile)
    print(romotename)


    ftp.UpLoadFiles(localzipfile, romotename,0)
    # ftp.close()
    try:
        os.remove(localfile)
        os.remove(localzipfile)
    except:
        pass
    ftp.ftp.cwd("..")
    romotefolder = 'texture/'
    # localfolder  = 'D:/Program Files (x86)/THD/Temp'
    root = (os.path.dirname(os.path.dirname(sys.argv[0])))
    root = root[0] + ':/'
    # print('root',root)
    localfolder = os.path.join(root, "texture_thd")

    texturefile = os.path.join(os.path.dirname(sys.argv[0]),'texture.txt')
    print(texturefile)
    # print("localfolder:"+localfolder)

    ftp.UpLoadtexture(localfolder, romotefolder, texturefile)
    ftp.close()
    # post 请求给平台
    print("ok!")

    # print("ok!")

def ftpuploadtexture():
    # ftp = myFtp('192.168.0.74', 21)
    # ftp.Login('zhf', '16696')

    ftp = myFtp('h.thd99.com',2121)
    ftp.Login('elarauser', '123456')

    romotefolder = 'texture/'
    # localfolder  = 'D:/Program Files (x86)/THD/Temp'
    root = (os.path.dirname(os.path.dirname(sys.argv[0])))
    root = root[0] + ':/'
    print('root',root)
    localfolder = os.path.join(root, "texture_thd")

    texturefile = os.path.join(os.path.dirname(sys.argv[0]),'texture.txt')
    print(texturefile)
    print('texturefilez:'+texturefile)
    print("localfolder:"+localfolder)

    ftp.UpLoadtexture(localfolder, romotefolder, texturefile)
    ftp.close()
    # post 请求给平台
    print("ok!")




if __name__ == "__main__":



    # print(a)
    a = 2017010305192210046
    value = random.randint(0, 100000)
    a = 20161209051910016 + value
    ftpuploadess(a)
    # ftpuploadtexture()

    # i = 0
    # while i < 1:
    #     value = random.randint(0, 100000)
    #     a = 20161209051910016 + value
    #     try:
    #         # ftpuploadhome(a)
    #
    #         ftpuploadess(a)
            # ftpuploadtexture()
    #     except Exception as err:
    #         print(err)
    #
    #     i = i + 1
    #     print("i",i)
    #     time.sleep(10)

        # break

    # ftpuploadfile(a)
    # ftp = myFtp('h.thd99.com',2121)
    # ftp.Login('elarauser', '123456')
    #
    # # romotefolder = 'upfile/' + time.strftime('%Y-%m-%d-%H-%M-%S/', time.localtime(time.time()))
    # # print(romotefolder)
    # romotefolder = 'uphome/' + str(a)
    # print(romotefolder)
    # localfolder  = 'D:/Program Files (x86)/THD/Temp'
    #
    # # ftp.DownLoadFileTree('f:/test/', '/test')  # ok
    # try:
    #     ftp.UpLoadFileTree(localfolder, romotefolder)
    # except Exception as err:
    #     print(err)
    #
