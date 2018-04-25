import Cryptodome
from Cryptodome import Random
from Cryptodome.Hash import SHA

from Cryptodome.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Cryptodome.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Cryptodome.PublicKey import RSA
import base64,os,sys
global tokenfile
from psutil import net_if_addrs
global macname
macname = ''

def get_mac_address():
    global macname
    # print("start")
    addr = []
    for k, v in net_if_addrs().items():
        for item in v:
            address = item[1]
            if '-' in address and len(address)==17:
                add1 = address.replace('-', '')
                addr.append(add1)
    print('addr',addr)

    # addr=['1C1B0DE82B74','1C1B0DE82B72','1C1B0DE82B76']
    namearray = []
    name = []
    # print("here")
    for item in addr:
        txtname= item + '.txt'
        name.append(txtname)
        txtpathname = os.path.join((os.path.dirname(sys.argv[0])), txtname)
        if os.path.isfile(txtpathname):
            print("textname",txtname)
            namearray.append(txtname)

            # os.path.isfile(txtname)
    macname = name[0]
    # print("macnamefirst",macname)
    print("name",name)
    if namearray:
        print('namearray',namearray)
        macname = namearray[0]
        if len(namearray) > 1:
            statinfo = os.stat(namearray[0]).st_mtime
            statinfo1 = os.stat(namearray[0]).st_mtime
            print("more than one")
            for item in namearray:
                statinfo = os.stat(item).st_mtime
                # print(os.stat(item).st_mtime,time.localtime(os.stat(item).st_mtime))
                if statinfo <= statinfo1:
                    macname = item
                statinfo1 = statinfo

    if macname:
        print(macname)
    else:
        print('not exist')
    return macname

try:
    get_mac_address()
except:
    pass

print('macname',macname )
if macname:
    tokenfile = os.path.join((os.path.dirname(sys.argv[0])), macname)
    print(tokenfile)
else:
    tokenfile=''
    print("tokenfile not exists")

# tokenfile = '1C1B0DE82B74.txt'


# #保存token
# token = 'U1B4QlhtNVUzMld6VE1TcWZVbElqckhJYmhJdmpYMTFHRXBDRkhyRkw0K0RoN2l4V1hDNVFGa3RrdWd1YllOQXFCVkVMdVMvMG55TDhWUzJTT3ZuTUo0UStySmJCL2luaU9raWZ5b0o5ekJyN2IweVJPQVRWcGNESG1xM3FJSi9tc2ZHb3FMS1BWNVZLVHQzWVNxdWZqMGI5SGZiVUc2Q1hWcS9rLzVnRDVjPQ=='
#
# with open(localfile, 'w+') as f:
#     f.write(token)

#token
privatepem = '-----BEGIN RSA PRIVATE KEY-----\nMIICXAIBAAKBgQCDXbmZ+rd+UvWW83xAD6mU01ub6KWB8YuD3BxeNx7UTy6LUSiwAiCE/JbWYkEFjSpos33iGksFhb1yIGok/u3/FBL8JIn4jkpTszzt4mvZajDwQ+8rPR3yAw5kDzawP3tJg3M6wLjXwINWBDI97JH/ZykEsSxToYwpqKpC5XkRXwIDAQABAoGATcFBJXHwAFaMRP/zsFtU7eE4nQzUQhi9kpvLMrz/g30muJGeOqfXpb94bIaVo/qNepGbViRn+WnS22VyTlmSdoOS+iWa/j4006r6s6ikzrhtkb044cs0N5Y5H+PdCpkXdnexKdfusi9s5CB17QfX1P+NnJZnKpR6fRM7nsGrfAkCQQDtMkAqGXco8XWyb4FFffcVUFYN/IFjohp6S+PxWV8JmWiFqqLLZC8/+1m+YswHFjPvf+fUzA0vlqAMwJ7+V5LbAkEAjce3sP45M/Z9X/9Rkpx2zFori61xCL4TWVFuVnf3VNi91A68XfEhfvXDkwfGVOB9k/SBD3vmkgaHCy6E22bozQJAXW2LpIl/TBs/ttcA3jRtnHGWU8//zxTMxRsbX7dKHefVKcE6ek6t5c/FW55iqu/t6QpCcKknEHWN+Tft6FTqPQJAcKD9Xc825f6j7oTG6m79OK1Q9m7b4pQMjuHPg0Vd57seYb0rCn2pnE/kA4MjnP2RBN4xQHmu2sXwtYNI63o+6QJBANdBoiqUV4OVyAFflqc8inhh0DrOZXuollILbiX6Vdj6gCutFFn6giuDQCQM3J82wChnvQS+cIxGHZpOham3LZc=\n-----END RSA PRIVATE KEY-----'
publicpem = '-----BEGIN RSA PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCDXbmZ+rd+UvWW83xAD6mU01ub6KWB8YuD3BxeNx7UTy6LUSiwAiCE/JbWYkEFjSpos33iGksFhb1yIGok/u3/FBL8JIn4jkpTszzt4mvZajDwQ+8rPR3yAw5kDzawP3tJg3M6wLjXwINWBDI97JH/ZykEsSxToYwpqKpC5XkRXwIDAQAB\n-----END RSA PUBLIC KEY-----'

def tokenmade():
    with open(tokenfile) as f:
        token = f.read()

    print(token)

    token = token.replace(' ','+').encode()

    # # # 伪随机数生成器
    random_generator = Random.new().read

    token = (base64.b64decode(token))
    print('\ntoken',token)


    rsakey = RSA.importKey(privatepem)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)

    res = []
    text = b''
    for i in range(0,len(token),128):
        # print(i,len(token),token[i:i+128])
        res.append(cipher.decrypt((token[i:i+128]), random_generator))

    for val in res:
        # print('decode text',val)
        text = text + val
    # text = text.decode()
    # print("\ntext",type(text))
    text = text.decode()
    print('text\n',type(text),text)

    import json
    te = json.loads(text)
    # print(type(te), te)

    message = te
    message['thd'] = 'zyyj'
    # print('message',message)

    # message = {"mid":"5d586ca2ef6224e9cb24f4b90d9ca998","account_type":2,"start_time":"2018-03-05 18:09:06","end_time":"2018-03-20 18:09:10","thd":"zyyj"}

    # print('message', message)


    message = json.dumps(message)
    # print('json',message)
    # json = json.loads(text)
    message = message.encode()
    print('message1',message)

    # print("public\n",publicpem)
    rsakey = RSA.importKey(publicpem)
    # print('rsakey',rsakey)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    res = []
    for i in range(0,len(message),117):
        # mes1 = cipher.encrypt(message)
        res.append(cipher.encrypt(message[i:i+117]))

    rest = b''
    for val in res:
        print('res',val)
        rest = rest+val
    print('rest:',rest)
    cipher_text = base64.b64encode(rest)
    # print('\ncipher_text',cipher_text)
    cipher_text = (cipher_text).decode()
    # cipher_text = base64.b64encode((cipher_text)).decode()
    # cipher_text = cipher_text.replace('+',' ')
    print('\ncipher_text', cipher_text)
    return cipher_text

if __name__ == '__main__':
    ltext = {"mid":"5d586ca2ef6224e9cb24f4b90d9ca998","account_type":2,"start_time":"2018-03-05 18:09:06","end_time":"2018-03-20 18:09:10","thd":"zyyj"}

    import time


    num = 3


    # url1 ='http://h5.thd.com/cloud/info/2017082105712310051.html?token=$[#UWN0UlJDQm9xU0crSXVMRkJBbmFYWTNCclhBdFZGRWdRajF2d3gvUVBMVDVETFFLak9OdGxlUkI3VDl4eVFvN1pkZ0Q0MVQ4ai9iWmdrak1wWEI3aDNsVEJ0QnBtUkRRbU9TZXlYcTMzVGY4QkxOODhCczJoZ2tTdjBTV3ZoTjVJOGV6MTdpaDBERnl0YklaTzJxZzdrR0FPTGlVcHVud0pDQldERUR6TTg4PQ==]$'


    if os.path.isfile(tokenfile) == True:
        urllist = ["http://h5.thd99.com:9999/unit", "http://h5.thd99.com:9999/win",
                   "http://h5.thd99.com:9999/farm","http://h5.91thd.com/unit?siid=100"]
        token = tokenmade()
        # print("token",token)
        url = urllist[num]+'?token=$[#'+token+']$'
        print('url',url)


    while True:
        print("test")
        time.sleep(5)










