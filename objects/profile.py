from helpers.database import get_profiles
from helpers.resy import get_auth_token
import random


# Load in a Profiles object
# Run random selection on the loaded profiles
# For each loaded profile get a new auth token

class Profiles:

    def __init__(self):
        profile_data = get_profiles()
        print(profile_data)
        if profile_data:
            self.profiles = [Profile(email=p['email'], password=p['password'], id=p['_id'], auth_token=p['auth_token']) for p in profile_data]
            print("loaded profiles...")
            self.active = True
        else:
            print("no profiles were loaded...")
            self.profiles = None
            self.active = False

    def random_selection(self):
        indexes = random.sample(range(len(self.profiles)), 3)
        self.profiles = [self.profiles[i] for i in indexes]
        print("random selected three profiles...")

    def update_tokens(self):
        for i in range(len(self.profiles)):
            self.profiles[i].get_new_token()
            print(f"Updated {self.profiles[i].email}'s auth token!")

class Profile:

    def __init__(self, email=None, password=None, id=None, auth_token=None):
        self.email = email
        self.password = password
        self.id = id
        self.auth_token = auth_token

    def get_new_token(self):
        if self.email and self.password:
            self.auth_token = get_auth_token(self.email, self.password)
        else:
            print("None value for email / password")
        