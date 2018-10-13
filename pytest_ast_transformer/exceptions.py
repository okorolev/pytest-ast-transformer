class TransformedNotFound(Exception):

    def __init__(self, msg):
        message = f'Transformed object not found. {msg}'

        self.message = message
        super().__init__(message)


class ContextIsRequired(Exception):

    def __init__(self):
        message = (
            'Set context to transformer. '
            'Help: `context = {}`'
        )

        self.message = message
        super().__init__(message)
