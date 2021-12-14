class DiffTypeError(TypeError):
    '''Raises if unix time difference has the wrong type'''
    def __init__(self, message):
        super().__init__(message)
