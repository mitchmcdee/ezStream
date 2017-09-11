import socket as s
import qrcode
from io import StringIO, BytesIO
from PIL import Image
import matplotlib.pyplot as plt
import time
import cv2
import numpy
import struct
import sys

plt.ion()

class Server:
    def __init__(self):
        self.socket = s.socket(s.AF_INET,s.SOCK_STREAM)
        self.socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
        self.socket.bind(('', 12345)) # TODO(mitch): change to 0 when done
        self.socket.listen(1)

        port = self.socket.getsockname()[1]
        print('waiting on connection on port', port)
        # qrcode.make(port).show()

    def waitForConnection(self):
        while True:
            connection = self.socket.accept()[0]
            if connection.recv(128) == b'HEYMAYUN': break
            connection.close()

        return connection

    def receiveImage(self, connection):
        connection.send(b'GET')

        metadataPacket = connection.recv(struct.calcsize("III"))
        length, width, height = struct.unpack("III", metadataPacket)
        # print('got metadata!', length, (width, height))

        buf = b''
        while True:
            buf += connection.recv(length)
            if len(buf) == length:
                break
        # print('got image! length =', len(buf))

        return Image.frombytes('RGB', (width, height), buf)

    def run(self):
        connection = self.waitForConnection()
        print('connected!')

        while True:
            start = time.time()
            image = self.receiveImage(connection)
            plt.imshow(image)
            plt.pause(sys.float_info.epsilon)
            fps = 1.0 / (time.time() - start)
            print(f'FPS: {fps:.4}')


if __name__ == '__main__':
    Server().run()        