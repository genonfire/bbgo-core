from django.utils.crypto import get_random_string

from core.testcase import TestCase
from utils.crypto import Crypto
from utils.text import Text


class CryptoTest(TestCase):
    def test_null_crypto(self):
        Crypto.cfb_encrypt(None)
        Crypto.cfb_decrypt(None)
        Crypto.cbc_encrypt(None)
        Crypto.cbc_decrypt(None)

    def test_cbc_encrypt_decrypt(self):
        samples = [
            get_random_string(23),
            get_random_string(32),
            get_random_string(50),
            get_random_string(127),
            12345678987654321,
        ]

        for sample in samples:
            coded_message = Crypto.cbc_encrypt(sample)
            message = Crypto.cbc_decrypt(coded_message)
            self.check(message, str(sample))

    def test_cfb_encrypt_decrypt(self):
        samples = [
            'aGCMobject',
            b'The cipher object has a read-only attribute: nounce.',
            '%s' % Text.UNABLE_TO_LOGIN,
        ]

        for sample in samples:
            coded_message = Crypto.cfb_encrypt(sample)
            assert (
                isinstance(coded_message, bytes) or
                isinstance(coded_message, bytearray)
            )

            message = Crypto.cfb_decrypt(coded_message)
            if isinstance(sample, bytes):
                sample = sample.decode('utf-8')
            self.check(message, sample)
