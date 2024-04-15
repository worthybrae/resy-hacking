class Profile:

    def __init__(self, email, password, _id=None, auth_token=None):
        self.email = email
        self.password = password
        self.id = _id
        self.auth_token = auth_token

    def get_new_token(self):
        return 