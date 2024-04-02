class BaseError(Exception):
    pass


class DatabaseError(BaseError):
    pass


class UnprocessableError(BaseError):
    pass
