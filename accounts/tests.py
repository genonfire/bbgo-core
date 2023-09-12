from django.utils import timezone

from core.testcase import TestCase as CoreTestCase

from . import models


class TestCase(CoreTestCase):
    def create_auth_code(
        self,
        email=None,
        tel=None,
        code='221014',
        created_at=None,
        is_used=False,
        used_at=None,
    ):
        if self.user and not email and not tel:
            email = self.user.username
        if not created_at:
            created_at = timezone.localtime()
        if not used_at:
            used_at = timezone.localtime()

        self.auth_code = models.AuthCode.objects.create(
            email=email,
            tel=tel,
            code=code,
            created_at=created_at,
            is_used=is_used,
            used_at=used_at
        )
        return self.auth_code
