
class _Const(object):
    """
    Common constants

    Reuseable constants as a boilerplate
    """

    KEY_MAX_LENGTH = 4
    FIELD_MAX_LENGTH = 20
    IP_ADDRESS_MAX_LENGTH = 45
    TEL_MAX_LENGTH = 100
    TITLE_MAX_LENGTH = 100
    PASSWORD_MAX_LENGTH = 128
    FILE_MAX_LENGTH = 128
    NAME_MAX_LENGTH = 150
    EMAIL_MAX_LENGTH = 254
    ADDRESS_MAX_LENGTH = 254
    URL_MAX_LENGTH = 1024
    DESC_MAX_LENGTH = 1024
    DIGITS_MAX_LENGTH = 12
    DECIMAL_PLACES_LENGTH = 6
    AUTH_CODE_LENGTH = 6
    AUTH_CODE_EXPIRATION_SECONDS = 900

    LENGTH_16 = 16
    LENGTH_32 = 32
    LENGTH_64 = 64
    LENGTH_128 = 128
    LENGTH_256 = 256
    LENGTH_512 = 512
    LENGTH_1024 = 1024

    BASE_ORDER = 0
    BASE_COUNT = 0

    MAX_LOOP = 999
    MAX_WORKERS = 8
    DEFAULT_PRECISION = 6
    DEFAULT_LINK_COUNT = 10

    FILTER_LIST_NAME = 'filter'

    QUERY_PARAM_TRUE = 'true'
    QUERY_PARAM_FALSE = 'false'
    QUERY_PARAM_ACTIVE = 'active'
    QUERY_PARAM_SEARCH = 'q'
    QUERY_PARAM_PK = 'pk'
    QUERY_PARAM_NAME = 'name'
    QUERY_PARAM_FORUM = 'forum'
    QUERY_PARAM_USED = 'used'
    QUERY_PARAM_SUCCESS = 'success'

    QUERY_PARAM_SORT = 'sort'
    QUERY_PARAM_SORT_LATEST = 'latest'
    QUERY_PARAM_SORT_EARLIEST = 'earliest'
    QUERY_PARAM_USERNAME_DSC = 'username_dsc'
    QUERY_PARAM_USERNAME_ASC = 'username_asc'

    TIME_FORMAT_DEFAULT = '%I:%M %p'
    MIME_TYPE_XLSX = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  # noqa
    EXCEL_FILENAME_FORMAT = '%Y%m%d%H%M%S'
    CENSORED_DATA = '******'
    CENSORED_EMAIL_DOMAIN = '@censo.red'

    REQUIRED = {'required': True, 'allow_null': False, 'allow_blank': False}
    NOT_NULL = {'allow_null': False, 'allow_blank': False}

    def __setattr__(self, name, value):
        raise AttributeError("cannot re-bind const(%s)" % name)


class _ConstProject(_Const):
    """
    Project constants

    Just for this project
    """

    LANG_SURNAME_AHEAD = [
        'ko',
    ]

    MAX_REPLY_NESTING = 99
    PERMISSION_TYPE = ['all', 'member', 'staff']
    P_READ = 'read'
    P_WRITE = 'write'
    P_REPLY = 'reply'

    SENSITIVE_URLS = [
        '/api/accounts/login/',
        '/api/accounts/signup/',
        '/api/accounts/password/change/',
        '/api/accounts/password/reset/',
    ]


Const = _ConstProject()
