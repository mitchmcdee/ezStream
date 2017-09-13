import struct
import qrcode
import sys
import time
import socket as s
import matplotlib.pyplot as plt
from secrets import token_bytes
from aes import AESCipher
from PIL import Image
from zlib import decompress
from multiprocessing import Queue, Process

plt.ion()

class Server:
    def __init__(self):
        self.socket = s.socket(s.AF_INET,s.SOCK_STREAM)
        self.socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
        self.socket.bind(('', 12345)) # TODO(mitch): change to 0 when done
        self.socket.listen(1)

        self.connection = None
        port = self.socket.getsockname()[1]
        self.plot = plt.imshow(qrcode.make(port))
        plt.axis('off')
        plt.pause(sys.float_info.epsilon)
        print('waiting on connection on port', port)
        print(token_bytes(16)) # TODO(mitch): use this as the password in QR code

    def waitForConnection(self):
        while True:
            connection = self.socket.accept()[0]
            if connection.recv(128) == b'HEYMAYUN': break
            connection.close()

        self.connection = connection

    def receiveImage(self):
        self.connection.send(b'GET')
        # print('getting!')

        metadataPacket = self.connection.recv(struct.calcsize("III"))
        length, width, height = struct.unpack("III", metadataPacket)
        print('got metadata!', length, (width, height))

        buf = b''
        while True:
            buf += self.connection.recv(length)
            if len(buf) == length:
                break
        # print('got image! length =', len(buf))

        return Image.frombytes('RGB', (width, height), decompress(AESCipher('hey').decrypt(buf)))

    def ImageWorker(self, framebuffer):
        while True:
            framebuffer.put(self.receiveImage())

    def run(self):
        self.waitForConnection()
        print('connected!')

        framebuffer = Queue()

        p = Process(target=self.ImageWorker, args=(framebuffer,))
        p.daemon = True
        p.start()

        start = time.time()
        while True:
            image = framebuffer.get()
            if image is None:
                continue

            self.plot.set_data(image)
            plt.axes().set_aspect(image.size[1] / image.size[0])
            plt.pause(sys.float_info.epsilon)

            fps = 1.0 / (time.time() - start)
            print(f'FPS: {fps:.4}')
            start = time.time()


if __name__ == '__main__':
    Server().run()        