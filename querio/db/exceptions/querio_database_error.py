
class QuerioDatabaseError(Exception):
    
    def __init__(self, message):
        self.message = message
        #Exception.__init__(self, None, None)

    def __str__(self):
        return self.message
        