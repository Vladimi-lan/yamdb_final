from django.contrib.auth.validators import UnicodeUsernameValidator


class NameMeValidator(UnicodeUsernameValidator):
    regex = r'^(?!me$)'
    message = 'Name "me" is forbidden.'
    flags = 0


username_validator = UnicodeUsernameValidator()
name_me_validator = NameMeValidator()
