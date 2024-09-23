from common.exceptions import BadRequestException


class UserHasNotEnoughFundsException(BadRequestException):
    default_message = (
        "User has not enough funds to proceed with the transaction"
    )
    error_code = "UserHasNotEnoughFundsError"


class TransactionAmountTooSmallException(BadRequestException):
    default_message = "Transaction total amount is too small to distribute"
    error_code = "TransactionAmountTooSmallError"
