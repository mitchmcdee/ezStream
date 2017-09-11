import socket
import pyscreenshot
from PIL import Image
from mss import mss
import numpy
from io import BytesIO
import struct
import cv2

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 12345))
s.send(b'HEYMAYUN')

capture = mss()
count = 0
while count < 5:
    print('waiting...')
    if s.recv(128) != b'GET': continue
    print('starting to send!')

    image = capture.grab(capture.monitors[1].copy())
    s.send(struct.pack("III", len(image.rgb), *image.size))
    s.sendall(image.rgb)

    print(f'sent image #{count}')
    count += 1