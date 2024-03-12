class UsersErrors(Exception):
    pass


class UserAlreadyExists(UsersErrors):
    pass


class UserNotFound(UsersErrors):
    pass
