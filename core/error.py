from rest_framework import serializers

from utils.text import Text


def ValidationError(code, field=''):
    message = getattr(Text, code)

    raise serializers.ValidationError(
        {
            'error': {
                'code': code,
                'message': message,
                'field': field,
            }
        }
    )


class Error(object):

    @staticmethod
    def invalid_page():
        ValidationError('INVALID_VALUE', 'page')

    @staticmethod
    def required_field(field):
        ValidationError('REQUIRED_FIELD', field)

    @staticmethod
    def alpha_number_only(field):
        ValidationError('ALPHABETS_NUMBER_ONLY', field)

    @staticmethod
    def you_must_consent(field=''):
        ValidationError('YOU_MUST_CONSENT', field)

    @staticmethod
    def invalid_password():
        ValidationError('INVALID_PASSWORD')

    @staticmethod
    def same_password():
        ValidationError('SAME_AS_OLD_PASSWORD')

    @staticmethod
    def invalid_uid():
        ValidationError('INVALID_UID')

    @staticmethod
    def invalid_token():
        ValidationError('INVALID_TOKEN')

    @staticmethod
    def unable_to_login():
        ValidationError('UNABLE_TO_LOGIN')

    @staticmethod
    def used_auth_code():
        ValidationError('USED_AUTH_CODE')

    @staticmethod
    def expired_auth_code():
        ValidationError('EXPIRED_AUTH_CODE')

    @staticmethod
    def invalid_auth_code():
        ValidationError('INVALID_AUTH_CODE')

    @staticmethod
    def file_not_exist(field):
        ValidationError('FILE_NOT_EXIST', field)

    @staticmethod
    def file_too_large():
        ValidationError('FILE_TOO_LARGE', 'file')

    @staticmethod
    def invalid_permission_type(attr=''):
        ValidationError('INVALID_PERMISSION_TYPE', attr)

    @staticmethod
    def vote_own_thread():
        ValidationError('ERROR_VOTE_OWN_THREAD')

    @staticmethod
    def vote_own_reply():
        ValidationError('ERROR_VOTE_OWN_REPLY')

    @staticmethod
    def invalid_category():
        ValidationError('INVALID_VALUE', 'category')

    @staticmethod
    def like_own_blog():
        ValidationError('ERROR_LIKE_OWN_BLOG')

    @staticmethod
    def already_liked():
        ValidationError('ERROR_LIKED_ALREADY')
