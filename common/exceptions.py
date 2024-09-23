class RootException(Exception):
    default_message = "Something went wrong"
    error_code = "ErrorCodeNotDefined"
    status_code = 500

    def __init__(self, message=None, error_field=None):
        self.message = message if message else self.default_message
        self.error_code = self.error_code
        self.error_field = error_field


class ObjectNotFoundException(RootException):
    default_message = "Object Not Found"
    error_code = "ObjectNotFound"
    status_code = 404


class BadRequestException(RootException):
    default_message = "Invalid Data Error"
    error_code = "InvalidDataError"
    status_code = 400


class ServiceUnavailableException(RootException):
    default_message = "Server Unavailable Error"
    error_code = "ServiceUnavailableError"
    status_code = 503

class InvalidUUIDException(BadRequestException):
    default_message = "Invalid UUID Error"
    error_code = "InvalidUUIDError"
