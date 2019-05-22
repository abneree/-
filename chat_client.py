from socket import *
import os,sys
import time

ADDR = (('127.0.0.1',8888))

# 发送信息
def send_msg(s,name):
    while True:
        try:
            txt = input("发言：")
        except KeyboardInterrupt:
            txt = "quit"
        if txt =="quit":
            msg = 'Q '+name
            s.sendto(msg.encode(),ADDR)
            sys.exit("退出聊天室")
        msg = "C %s %s"%(name,txt)
        s.sendto(msg.encode(),ADDR)
        time.sleep(3)
# 接收
def recv_msg(s):
    while True:
        data,addr = s.recvfrom(2048)
        if data.decode()=="EXIT":
            sys.exit()
        print(data.decode())

# 搭建网络
def main():
    s = socket(AF_INET,SOCK_DGRAM)
    while True:
        name = input("请输入姓名：")
        msg = "L "+name
        s.sendto(msg.encode(),ADDR)
        data,addr = s.recvfrom(1024)
        if data.decode() == 'OK':
            print("你已进入聊天室")
            break
        else:
            print(data.decode())

    # 实现多进程，子进程发送，父进程接收
    pid = os.fork()
    if pid < 0:
        sys.exit("Error")
    elif pid ==0:
        send_msg(s,name)
    else:
        recv_msg(s)

if __name__ == '__main__':
    main()
