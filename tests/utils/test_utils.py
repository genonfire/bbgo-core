from django.conf import settings

from core.testcase import TestCase
from utils.constants import Const
from utils import datautils
from utils.debug import Debug
from utils.text import Text
from utils.regexp import RegExpHelper


class UtilTest(TestCase):
    def test_set_const(self):
        result = False
        try:
            Const.NAME_MAX_LENGTH = 0
        except AttributeError:
            result = True

        try:
            Text.INVALID_TOKEN = 'Invalid Token'
        except AttributeError:
            result = True

        self.check(result)

    def test_print(self):
        result = False
        if Debug.test_mode():
            if not Debug._trace_enabled():
                settings.TRACE_ENABLED = True
            Debug.trace('\nTrace test.')
            Debug.error('Error test.')
            Debug.print('Print test.')
            settings.TRACE_ENABLED = False
            result = True

        self.check(result)

        result = False
        if Debug.debug_or_test_mode():
            if not Debug.debug_mode():
                settings.DEBUG = True
            Debug.loooog('Log test.')
            Debug.callstack(limit=0)
            settings.DEBUG = False
            result = True

        self.check(result)

    def test_regexp(self):
        self.check(RegExpHelper.is_numbers('1234567890'))
        self.check_not(RegExpHelper.is_numbers('123-4567890'))
        self.check(RegExpHelper.numbers('010-1234-5678'), '01012345678')
        self.check_not(RegExpHelper.is_numbers(''))

        self.check(RegExpHelper.is_alphanumerics('abcdeFGHJKL9876'))
        self.check_not(RegExpHelper.is_alphanumerics('abcde@'))
        self.check_not(RegExpHelper.is_alphanumerics(''))
        self.check(RegExpHelper.alphanumerics('a@b.com'), 'abcom')

        self.check(RegExpHelper.is_uniwords('abc-123_Z'))
        self.check_not(RegExpHelper.is_uniwords('abc@'))
        self.check_not(RegExpHelper.is_uniwords(''))


class DataUtilsTest(TestCase):
    def test_search_dict(self):
        list_of_dict = [
            {
                'id': 0,
                'value': 2
            },
            {
                'id': 1,
                'value': 1
            },
            {
                'id': 2,
                'value': 0
            },
        ]
        item = datautils.search_dict('id', 0, list_of_dict)
        self.check(item.get('id'), 0)
        self.check(item.get('value'), 2)

        item = datautils.search_dict('dummy', 1, list_of_dict)
        self.check_not(item)

        item = datautils.search_dict('value', 0, list_of_dict)
        self.check(item.get('id'), 2)
        self.check(item.get('value'), 0)

        value = datautils.get_object_from_dict(item, 'value')
        self.check(value, 0)

    def test_true_or_false(self):
        samples = [
            'true',
            'True',
            'false',
            'False',
            True,
            False,
            'Nothing',
        ]
        values = [
            'True',
            'True',
            'False',
            'False',
            None,
            None,
            None,
        ]

        for (sample, value) in zip(samples, values):
            true_or_false = datautils.true_or_false(sample)
            self.check(true_or_false, value)

    def test_normal_round(self):
        samples = [
            2.49999,
            2.50000,
            2.50001,
        ]
        values = [
            2,
            3,
            3,
        ]

        for (sample, value) in zip(samples, values):
            true_or_false = datautils.normal_round(sample)
            self.check(true_or_false, value)

    def test_div_prec(self):
        result = datautils.div_prec(1, 7, 6)
        self.check(result, datautils.decimal.Decimal('0.142857'))

        result = datautils.div_prec(1, 0)
        self.check(result, 0)

    def test_divide_or_zero(self):
        result = datautils.divide_or_zero(4, 2)
        self.check(result, 2)

        result = datautils.divide_or_zero(4, 0)
        self.check(result, 0)
