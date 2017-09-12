import socket as s
import qrcode
from PIL import Image
import matplotlib.pyplot as plt
import time
import struct
import sys
from aes import AESCipher

plt.ion()

class Server:
    def __init__(self):
        self.socket = s.socket(s.AF_INET,s.SOCK_STREAM)
        self.socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
        self.socket.bind(('', 12345)) # TODO(mitch): change to 0 when done
        self.socket.listen(1)

        port = self.socket.getsockname()[1]
        self.plot = plt.imshow(qrcode.make(port))
        plt.axis('off')
        plt.pause(sys.float_info.epsilon)
        print('waiting on connection on port', port)

    def waitForConnection(self):
        while True:
            connection = self.socket.accept()[0]
            if connection.recv(128) == b'HEYMAYUN': break
            connection.close()

        return connection

    def receiveImage(self, connection):
        connection.send(b'GET')
        # print('getting!')

        metadataPacket = connection.recv(struct.calcsize("III"))
        length, width, height = struct.unpack("III", metadataPacket)
        # print('got metadata!', length, (width, height))

        buf = b''
        while True:
            buf += connection.recv(length)
            if len(buf) == length:
                break
        # print('got image! length =', len(buf))

        return Image.frombytes('RGB', (width, height), AESCipher('hey').decrypt(buf))

    def run(self):
        connection = self.waitForConnection()
        print('connected!')

        while True:
            start = time.time()
            image = self.receiveImage(connection)

            self.plot.set_data(image)
            plt.axes().set_aspect(image.size[1] / image.size[0])
            plt.pause(sys.float_info.epsilon)

            fps = 1.0 / (time.time() - start)
            print(f'FPS: {fps:.4}')


if __name__ == '__main__':
    Server().run()        