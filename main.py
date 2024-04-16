from objects.profile import Profiles
from helpers.database import get_restaurants, get_tables


def initialize(reservation_mins):
    profiles_obj = Profiles()
    if profiles_obj.active:
        print(len(profiles_obj.profiles))
        profiles_obj.random_selection()
        print(len(profiles_obj.profiles))
        profiles_obj.update_tokens()
        restaraunts_data = get_restaurants()
        venues = [x.venue_id for x in restaraunts_data]
        tables_data = get_tables(venues)
        



initialize(540)