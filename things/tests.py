from core.testcase import TestCase as CoreTestCase

from . import models


class TestCase(CoreTestCase):
    def create_attachment(
        self,
        name='test.txt',
        content=b'test',
        content_type='text/plain'
    ):
        file = self.file(name, content, content_type)

        self.attachment = models.Attachment.objects.create(
            file=self.file(name, content, content_type),
            content_type=file.content_type,
            size=file.size
        )
        return self.attachment
