class TransformedNotFound(Exception):

    def __init__(self, *, func, cls='<Not expected>'):
        message = (
            'Transformed object not found. '
            f'Func: {func} '
            f'Class: {cls}'
        )

        self.cls = cls
        self.func = func
        self.message = message
        super().__init__(message)
