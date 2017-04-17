import numpy as np
import cv2
import socket
import struct
CLIENT_IP='10.42.0.1'
CLIENT_PORT = 50677
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#sock.bind((CLIENT_IP, CLIENT_PORT))
sock.bind(('', CLIENT_PORT))
pic=''
temp=-1
while True:
    temp=-1
    flag=0
    while True:
        data, addr = sock.recvfrom(20480)
        seq=struct.unpack('I',data[0:4])[0]
        try:
            if struct.unpack('I',data[4:8])[0]==9999:
                break
        except:
            pass
        if seq-1>temp:
            print 'error'
            flag=1
        temp=seq
        pic=pic+data[4:]
    if seq != temp+1:
        flag=1
    try:
        if flag==0:
            img=cv2.imdecode(np.asarray(bytearray(pic),dtype=np.uint8), 1)
            res = cv2.resize(img,None,fx=1, fy=1, interpolation = cv2.INTER_CUBIC)
    except:
        flag=1
    try:
        if flag==0:
            cv2.imshow('frame',res)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break;
    except:
        pass
    pic=''

