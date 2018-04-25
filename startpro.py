# -*- coding:utf-8 -*-
import subprocess ,os,sys
from time import sleep
import shutil

path = sys.argv[0]
print("path:",path)

path = (os.path.dirname(sys.argv[0]))
root = path[0] + ':/'
print("root:",path,root)

dest = root + "/upload"

shutil.copy(path, dest)


localfile =root + "/upload/upload.exe 5"

print('localfile:' + localfile)

while True:
    print("path:", path)
    sleep(5)
# subprocess.call(localfile)