from player_create import player, player_continue
from tutorial import play_prologue
from travel import  where_to_travel
from battles import battle_start
from animation import plane_animation, logo
from location_update import update_location


def main():
    logo()
    screen_name, is_new_player, location, player_id = player()
    if is_new_player == 1:
        play_prologue(screen_name)
    while True:
        location = update_location(screen_name)
        near_airports_list, screen_name = player_continue(screen_name, location)
        airport_ident, screen_name = where_to_travel(near_airports_list, screen_name)
        plane_animation()
        battle_start(screen_name, airport_ident)


if __name__ == "__main__":
    main()
