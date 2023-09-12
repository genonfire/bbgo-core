import decimal

from utils.constants import Const
from utils.debug import Debug  # noqa


def search_dict(key, value, list_of_dict):
    for item in list_of_dict:
        try:
            if item[key] == value:
                return item
        except KeyError:
            return None


def get_object_from_dict(data, key='id', default=None):
    if data:
        return data.get(key, default)
    return default


def true_or_false(param):
    if param == 'true' or param == 'True':
        return 'True'
    elif param == 'false' or param == 'False':
        return 'False'
    else:
        return None


def normal_round(value):
    decimal.getcontext().rounding = decimal.ROUND_HALF_UP
    return decimal.Decimal(value).to_integral_value()


def div_prec(a, b, prec=Const.DEFAULT_PRECISION):
    if b == 0:
        return 0

    decimal.getcontext().rounding = decimal.ROUND_HALF_UP
    decimal.getcontext().prec = prec
    return decimal.Decimal(a) / decimal.Decimal(b)


def divide_or_zero(a, b):
    if b:
        return a / b
    else:
        return 0
