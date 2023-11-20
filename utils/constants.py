
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
    QUERY_PARAM_DELETED = 'delete'

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
    JSON_REQUIRED = {'required': True, 'allow_null': False}
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

    QUERY_PARAM_PINNED = 'pin'
    QUERY_PARAM_SORT_UP = 'up'
    QUERY_PARAM_SORT_DOWN = 'down'
    QUERY_PARAM_CATEGORY = 'category'
    QUERY_PARAM_TAG = 'tag'

    PERMISSION_LIST = [
        'permission_list',
        'permission_read',
        'permission_write',
        'permission_reply',
        'permission_vote',
    ]
    PERMISSION_ALL = 'all'
    PERMISSION_MEMBER = 'member'
    PERMISSION_STAFF = 'staff'
    PERMISSION_TYPE = [
        PERMISSION_ALL,
        PERMISSION_MEMBER,
        PERMISSION_STAFF,
    ]

    FORUM_OPTION_DEFAULT = {
        'permission_list': PERMISSION_MEMBER,
        'permission_read': PERMISSION_MEMBER,
        'permission_write': PERMISSION_MEMBER,
        'permission_reply': PERMISSION_MEMBER,
        'permission_vote': PERMISSION_MEMBER,
        'support_files': False,
    }
    BLOG_OPTION_DEFAULT = {
        'permission_list': PERMISSION_ALL,
        'permission_read': PERMISSION_ALL,
        'permission_write': PERMISSION_STAFF,
        'permission_reply': PERMISSION_ALL,
        'permission_vote': PERMISSION_ALL,
    }

    MAX_REPLY_NESTING = 99

    SENSITIVE_URLS = [
        '/api/accounts/login/',
        '/api/accounts/signup/',
        '/api/accounts/password/change/',
        '/api/accounts/password/reset/',
    ]


Const = _ConstProject()
