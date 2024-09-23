from common.exceptions import ObjectNotFoundException


class UserNotFoundException(ObjectNotFoundException):
    default_message = "User not found"
    error_code = "UserNotFound"
