
from search_db import search_db


def update_location(screen_name):
    location = search_db(f"SELECT location FROM player WHERE screen_name = '{screen_name}'")[0][0]
    return location
