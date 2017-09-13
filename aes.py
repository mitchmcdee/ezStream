from hashlib import md5
from base64 import b64decode
from base64 import b64encode
from Crypto import Random
from Crypto.Cipher import AES
from secrets import token_bytes

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * bytes(chr(BLOCK_SIZE - len(s) % BLOCK_SIZE), encoding='utf-8')
unpad = lambda s: s[:-ord(s[-1:])]

class AESCipher:
    def __init__(self, key):
        # self.key = key
        self.key = md5(key.encode('utf8')).hexdigest()

    def encrypt(self, raw):
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted = b64encode(iv + cipher.encrypt(raw))
        return encrypted

    def decrypt(self, enc):
        enc = b64decode(enc)
        iv = enc[:BLOCK_SIZE]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(enc[BLOCK_SIZE:]))
        return decrypted