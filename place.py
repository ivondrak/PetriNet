class Place:
    def __init__(self, name, initial=0):
        self.name = name
        self.tokens = initial

    def get_tokens(self):
        return self.tokens

    def add_token(self):
        self.tokens += 1

    def remove_token(self):
        if self.tokens > 0:
            self.tokens -= 1

    def print(self):
        print("Place " + self.name + " has " + str(self.tokens) + " token(s)")
