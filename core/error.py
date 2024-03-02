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
    def invalid_page():
        ValidationError('INVALID_VALUE', 'page')

    def required_field(field):
        ValidationError('REQUIRED_FIELD', field)

    def alpha_number_only(field):
        ValidationError('ALPHABETS_NUMBER_ONLY', field)

    def you_must_consent(field=''):
        ValidationError('YOU_MUST_CONSENT', field)

    def invalid_password():
        ValidationError('INVALID_PASSWORD')

    def same_password():
        ValidationError('SAME_AS_OLD_PASSWORD')

    def invalid_uid():
        ValidationError('INVALID_UID')

    def invalid_token():
        ValidationError('INVALID_TOKEN')

    def unable_to_login():
        ValidationError('UNABLE_TO_LOGIN')

    def used_auth_code():
        ValidationError('USED_AUTH_CODE')

    def expired_auth_code():
        ValidationError('EXPIRED_AUTH_CODE')

    def invalid_auth_code():
        ValidationError('INVALID_AUTH_CODE')

    def file_not_exist(field):
        ValidationError('FILE_NOT_EXIST', field)

    def file_too_large():
        ValidationError('FILE_TOO_LARGE', 'file')

    def invalid_permission_type(attr=''):
        ValidationError('INVALID_PERMISSION_TYPE', attr)

    def vote_own_thread():
        ValidationError('ERROR_VOTE_OWN_THREAD')

    def vote_own_reply():
        ValidationError('ERROR_VOTE_OWN_REPLY')

    def invalid_category():
        ValidationError('INVALID_VALUE', 'category')

    def like_own_blog():
        ValidationError('ERROR_LIKE_OWN_BLOG')

    def already_liked():
        ValidationError('ERROR_LIKED_ALREADY')
