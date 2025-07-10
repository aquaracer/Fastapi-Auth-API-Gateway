class UserNotFoundExceptionError(Exception):
    details = "User not found"


class UserNotCorrectPasswordExceptionError(Exception):
    details = "Password is not correct"


class TokenExpiredError(Exception):
    detail = "Token has expired"


class TokenNotCorrectError(Exception):
    detail = "Token is not correct"


class TaskNotFoundError(Exception):
    detail = "Task not found"
