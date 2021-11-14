class BankException(Exception):
    """For all exceptions related to this project. """
    def __init__(self, message):
        super.__init__(message)