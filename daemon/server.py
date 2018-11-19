import socket
import sys
from datetime import datetime
import os

PID = os.getpid()
UDP_IP = "127.0.0.1"
UDP_PORT = 5005


def log(s):
    #print(datetime.now().strftime('[%Y/%m/%d-%H:%M] ')+'['+str(PID)+'] '+s)
    print(s)
    sys.stdout.flush()


try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
    sock.bind((UDP_IP, UDP_PORT))
except Exception as e:
    log('=== Server already running')
    sys.exit(-1)

log('>>> Server started')
try:
    log('Socket created')

    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        log('Received: '+data.strip())
    sys.exit(0)

except Exception as e:
    #log('Exception: '+str(e.args[0])+e.strerror)
    log('Exception: '+str(e.strerror))
    log('<<< Server stopped')
    sys.exit(-1)

