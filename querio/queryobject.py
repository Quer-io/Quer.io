

class QueryObject:

    def __init__(self, target):
        self.target = target
        self.expression = None

    def add(self, expression):
        if self.expression is None:
            self.expression = expression
        else:
            self.expression = self.expression & expression
