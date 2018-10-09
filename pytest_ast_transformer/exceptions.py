class TransformedNotFound(Exception):

    def __init__(self, *, func, cls='<Not expected>'):
        message = (
            'Transformed object not found. '
            f'Func: {func} '
            f'Class: {cls}'
        )

        super().__init__(message)
