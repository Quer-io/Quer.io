
class QuerioDatabaseError(Exception):
    
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, args, kwargs)

    def __str__(self):
        if len(self.args) == 0:
            return ""
        
        return str(self.args[0][0])
        