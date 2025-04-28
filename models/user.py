class User:
    def __init__(self, username, password, first_name, last_name, address, balance=0):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.balance = balance
        self.role = None  # Will be defined in child classes

    def __eq__(self, other):
        return isinstance(other, User) and self.username == other.username
        