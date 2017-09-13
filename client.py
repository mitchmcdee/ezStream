import socket
from mss import mss
import struct
from aes import AESCipher
from zlib import compress

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 12345))
s.send(b'HEYMAYUN')

capture = mss()
# size = capture.monitors[1]
size = {'left': 0, 'top': 0, 'width': 365, 'height': 670}
count = 0
while True:
    if s.recv(128) != b'GET': continue
    print('starting to send!')

    image = capture.grab(size.copy())
    message = AESCipher('hey').encrypt(compress(image.rgb))
    s.send(struct.pack("III", len(message), *image.size))
    s.sendall(message)

    print(f'sent image #{count}')
    count += 1