from django.db import models

from utils.crypto import Crypto


class EncryptedFieldMixin(object):
    def from_db_value(self, value, expression, connection):
        return self.to_python(Crypto.cbc_decrypt(value))

    def get_prep_value(self, value):
        value = super(EncryptedFieldMixin, self).get_prep_value(value)
        return Crypto.cbc_encrypt(value)


class EncryptedCharField(EncryptedFieldMixin, models.CharField):
    """
    It is strongly recommended to set max_length to at least twice
    the intended length for encryption varying.
    """
    pass
