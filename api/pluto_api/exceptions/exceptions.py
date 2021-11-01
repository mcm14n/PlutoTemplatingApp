class AppError(Exception):
    """ General Error for Application """

    def __init__(self, message, status=500):
        self.message = message
        self.status = status
