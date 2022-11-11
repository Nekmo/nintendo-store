

class FonException(Exception):
    pass


class InvalidLogin(FonException):
    pass


class TimeClockUnavailable(FonException):
    pass
