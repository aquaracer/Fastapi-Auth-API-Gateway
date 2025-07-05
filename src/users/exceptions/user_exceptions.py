class UserNotFoundException(Exception):
    details = "User not found"


class UserNotCorrectPasswordException(Exception):
    details = "Password is not correct"


class TokenExpired(Exception):
    detail = "Token has expired"


class TokenNotCorrect(Exception):
    detail = "Token is not correct"


class TaskNotFound(Exception):
    detail = "Task not found"
