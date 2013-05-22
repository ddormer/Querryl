class SearchError(Exception):
    """
    An error for L{querryl.providers}.
    """
    def __init__(self, message, errorCode=None):
       Exception.__init__(self, message)
       self.errorCode = errorCode
