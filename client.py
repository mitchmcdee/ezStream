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
# size = capture.monitors[1]
size = {'left': 0, 'top': 0, 'width': 365, 'height': 670}
count = 0
while True:
    if s.recv(128) != b'GET': continue
    print('starting to send!')

    image = capture.grab(size.copy())
    s.send(struct.pack("III", len(image.rgb), *image.size))
    s.sendall(image.rgb)

    print(f'sent image #{count}')
    count += 1