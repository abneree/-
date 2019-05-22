from socket import *
import os
import time

# 服务器地址
ADDR = (('127.0.0.1',8888))
user = {}

# 接收请求并解析
def do_request(s):
    while True:
        data,addr = s.recvfrom(1024)
        msg = data.decode().split(" ")
        if msg[0] =="L":
            do_login(s,msg[1],addr)
        elif msg[0]=="C":
            do_chat(s,msg)
        elif msg[0] == "Q":
            do_quit(s,msg[1])

# 退出
def do_quit(s,name):
    msg = "%s退出聊天室"%name
    for i in user:
        if i !=name:
            s.sendto(msg.encode(),user[i])
        else:
            s.sendto(b'EXIT', user[i])

    del user[name]

# 发言
def do_chat(s,msg):
    name = msg[1]
    txt = " ".join(msg[2:])
    ms = "%s:%s"%(name,txt)
    for i in user:
        s.sendto(ms.encode(),user[i])

# 进入
def do_login(s,name,addr):
    if name in user:
        s.sendto("该用户已经存在".encode(),addr)
        return
    s.sendto(b'OK',addr)
    msg = "欢迎%s进入聊天室"%name
    for i in user:
        s.sendto(msg.encode(),user[i])

    user[name] = addr


# 创建网络连接
def main():
    s = socket(AF_INET,SOCK_DGRAM)
    s.bind(ADDR)

    pid = os.fork()
    if pid<0:
        return
    elif pid ==0:
        while True:
            msg =input("管理员：")
            txt = "C %s %s"%("管理员",msg)
            s.sendto(txt.encode(),ADDR)
            time.sleep(3)
    else:
        do_request(s)


if __name__ == '__main__':
    main()