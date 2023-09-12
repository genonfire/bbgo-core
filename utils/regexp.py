import re


class _RegExpHelper(object):
    def is_numbers(self, data):
        if not data:
            return False
        return re.match(r'^[0-9]*$', data)

    def is_alphanumerics(self, data):
        if not data:
            return False
        return re.match(r'^[a-zA-Z0-9]*$', data)

    def is_uniwords(self, data):
        if not data:
            return False
        return re.match(r'^[a-zA-Z0-9_-]*$', data)

    def numbers(self, data):
        return re.sub(r'[^0-9]', '', data)

    def alphanumerics(self, data):
        return re.sub(r'[^a-zA-Z0-9]', '', data)


RegExpHelper = _RegExpHelper()
