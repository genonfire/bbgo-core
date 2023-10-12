from django.utils import translation
from django.utils.translation import gettext_lazy as _


class _Text(object):
    """
    Common text

    Reuseable text as a boilerplate
    """

    UNABLE_TO_LOGIN = _("Unable to login.")
    USER_IS_DEACTIVATED = _("User is deactivated.")
    INVALID_PASSWORD = _("Invalid password.")
    SAME_AS_OLD_PASSWORD = _("Same as old password.")
    USER_NOT_EXIST = _("User not exist.")
    USERNAME_EXISTS = _("Username exists.")
    INVALID_UID = _("Invalid uid.")
    INVALID_TOKEN = _("Invalid token.")
    YOU_MUST_CONSENT = _("You must consent.")

    INVALID_PERMISSION_TYPE = _("Invalid permission type")
    ALPHABETS_NUMBER_ONLY = _("alphabets and number only")
    USED_AUTH_CODE = _("Used auth code.")
    EXPIRED_AUTH_CODE = _("Expired auth code.")
    INVALID_AUTH_CODE = _("Invalid auth code.")
    MSG_SMS_AUTHENTICATE = _('Authenticate code. %(code)s')

    REQUIRED_FIELD = _("This field is required.")
    INVALID_VALUE = _("Invalid value")
    FILE_TOO_LARGE = _("File too large")
    ALREADY_EXISTS = _("Already exists.")
    FILE_NOT_EXIST = _("File does not exist.")

    EXCEL_TITLE_USER = _("User")
    EXCEL_TITLE_USERNAME = _("Username")
    EXCEL_TITLE_FIRSTNAME = _("First name")
    EXCEL_TITLE_LASTNAME = _("Last name")
    EXCEL_TITLE_CALLNAME = _("Call Name")
    EXCEL_TITLE_TEL = _("Tel")
    EXCEL_TITLE_ADDRESS = _("Address")
    EXCEL_TITLE_ACTIVE = _("Active")
    EXCEL_TITLE_APPROVED = _("Approved")
    EXCEL_TITLE_JOINED_DATE = _("Joined at")

    def __setattr__(self, name, value):
        raise AttributeError("cannot re-bind text(%s)" % name)

    def language(self):
        return translation.get_language()

    def activate(self, language=None):
        if not language:
            language = self.language()
        return translation.activate(language)

    def get(self, text):
        return _(text)


class _TextProject(_Text):
    """
    Project text

    Just for this project
    """

    ERROR_VOTE_OWN_THREAD = _("Can't vote own thread.")
    ERROR_VOTE_OWN_REPLY = _("Can't vote own reply.")


Text = _TextProject()
