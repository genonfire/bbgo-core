from base64 import b64encode, b64decode
from binascii import (
    a2b_hex,
    b2a_hex
)
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad

from django.conf import settings

from utils.debug import Debug  # noqa


class _Crypto(object):
    def key(self):
        return settings.AES_PASSPHRASE.encode('utf-8')[:16]

    def cbc_encrypt(self, text):
        if not text:
            return None

        key = self.key()
        cryptor = AES.new(key, AES.MODE_CBC, key)

        if isinstance(text, str):
            text = text.encode()
        elif isinstance(text, int):
            text = str(text).encode()

        ciphertext = cryptor.encrypt(pad(text, AES.block_size))
        return b2a_hex(ciphertext).decode('utf-8')

    def cbc_decrypt(self, ciphertext):
        if not ciphertext:
            return None

        key = self.key()
        cryptor = AES.new(key, AES.MODE_CBC, key)
        text = unpad(cryptor.decrypt(a2b_hex(ciphertext)), AES.block_size)
        return bytes.decode(text)

    def cfb_encrypt(self, text):
        if not text:
            return None

        key = self.key()
        if isinstance(text, str):
            byte_message = bytearray(text, 'utf-8')
        else:
            byte_message = text

        aes = AES.new(key, AES.MODE_CFB, key)
        return b64encode(aes.encrypt(byte_message))

    def cfb_decrypt(self, ciphertext):
        if not ciphertext:
            return None

        key = self.key()
        aes = AES.new(key, AES.MODE_CFB, key)
        return aes.decrypt(b64decode(ciphertext)).decode('utf-8')


Crypto = _Crypto()
