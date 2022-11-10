class DatabaseAlreadyExists(BaseException):
    pass


class CollectionAlreadyExists(BaseException):
    pass


class DatabaseDoesNotExist(BaseException):
    pass


class CollectionDoesNotExist(BaseException):
    pass
