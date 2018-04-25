# -*- coding: utf-8 -*-
from time import sleep
import time,datetime
import os,sys


def ctime():
    FMT = '%Y-%m-%d %H:%M:%S'
    return time.strftime(FMT, time.localtime())


def log_message(path, hit, text=''):
    try:
        file = open(path, 'a+')
        file.write('%s %s\t%s' % (ctime(), hit, text))
    finally:
        if file:
            file.close()

def initlog(logfile):  # 日志
    import logging
    logger = logging.getLogger()
    hdlr = logging.FileHandler(logfile)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger


def getpath(addr):

    # print(sys.argv[0])
    BASE_DIR = (os.path.dirname(sys.argv[0]))
    LOG_DIR = os.path.join(BASE_DIR, "logs")
    # print(LOG_DIR)
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)  # 创建路径

    LOG_FILE = addr + ".log"
    path = os.path.join(LOG_DIR, LOG_FILE)
    # path = LOG_DIR +'/'+ LOG_FILE
    return path

homepath   = getpath("uploadhome")
# print("homepath"+homepath)
filepath   = getpath("uploadfile")
# print("filepath"+filepath)
designpath = getpath("uploaddesign")
# print("designpath"+designpath)

# print("here")
path = [homepath,filepath,designpath]
print("path",path)

if __name__ == '__main__':


    log_message(homepath, "test", "456"+'\n')
    log_message(filepath, "test", "456" + '\n')
    log_message(designpath, "test", "456" + '\n')


