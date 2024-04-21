import random
import time
import colorama

from geopy.distance import geodesic
from search_db import search_db
from input_validation import input_check
from inventory import create_inventory
from itemsearch import search_airport
from travel import travel_choice
from battles import clear_screen
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

def search_player():
    #search player
    #lisätty että jos vanhaa nimeä ei löydy, kutsuu tätä funktiota uudelleen
    name = input("Insert your player name: ").upper()
    print(f"{name}\n\n")
    sql = f"SELECT id, screen_name, location FROM player WHERE screen_name = '{name}'"
    result = search_db(sql)

    if result:
        # print(f"Player info: {first_result}")
        player_id = result[0][0]
        screen_name = result[0][1]
        location = result[0][2]
        return screen_name, location, player_id
    else:
        print(f"{name} player not found.")
        return search_player()



def add_new_player(player_name, location_ident, inventory_id, yhteys):
    #lisätty tarkistus-funktio check_player_name että onko nimi jo käytössä, kutsuu myös create inventorya
    name = player_name
    name = player_name_check(name)
    # inventory_id = create_inventory()
    location_ident = start_country()
    destination_ident = player_destination(location_ident)
    sql = f"INSERT INTO player (screen_name, player_lvl, battles_won, experience, location, inventory_id, destination, player_health) VALUES ('{name}', 1, 0, 0, '{location_ident}', '{inventory_id}', '{destination_ident}', 100)"
    search_db(sql)
    player_id = search_db(f"SELECT player.id FROM player WHERE screen_name = '{name}'")
    print(f"{name} player added.")
    return name, location_ident, player_id



def player():
    answer = input("Are you a new(1) or an existing player(2): ")

    choice = input_check(answer, 2)

    if choice == 1:
        name, location, player_id = add_new_player()
        is_new_player = 1
    elif choice == 2:
        name, location, player_id = search_player()
        is_new_player = 0
    return name, is_new_player, location, player_id


def player_name_check(name):
    name_list = []
    sql = "SELECT screen_name FROM player"
    result = search_db(sql)

    for i in result:
        name_list.append(i[0])

    while True:
        if name in name_list:
            name = input("The name is already in use. Please choose a different name: ").upper()
        else:
            break

    return name


def start_country():
    sql = "SELECT country.name, count(*) FROM country, airport WHERE airport.iso_country = country.iso_country GROUP BY country.iso_country HAVING count(*) > 29 AND count(*) < 118 ORDER BY count(*) DESC"
    countries = search_db(sql)
    random_country = countries[random.randint(0, len(countries)-1)][0]
    return start_airport(random_country)


def start_airport(country):
    sql = f"SELECT airport.name FROM airport, country WHERE airport.iso_country = country.iso_country AND country.name = '{country}' AND difficulty = 1"
    airports = search_db(sql)
    player_location = airports[random.randint(0, len(airports)-1)][0]
    sql = f"SELECT airport.ident FROM airport WHERE airport.name = '{player_location}'"
    ident_search = search_db(sql)
    location_ident = ident_search[0][0]
    return location_ident


def player_destination(location_ident):
    sql = f"SELECT latitude_deg, longitude_deg FROM airport WHERE airport.ident = '{location_ident}'"
    location1 = search_db(sql)
    sql = f"SELECT country.name FROM country, airport WHERE country.iso_country = airport.iso_country and airport.ident = '{location_ident}'"
    country = search_db(sql)[0][0]
    sql = f"SELECT airport.ident, latitude_deg, longitude_deg, difficulty FROM airport, country WHERE airport.iso_country = country.iso_country AND country.name = '{country}' AND airport.ident != '{location_ident}'"
    airports = search_db(sql)
    airports_dict = {}

    for row in airports:
        location2 = row[1], row[2]
        airports_dict.update({round(geodesic(location1, location2).km, 3):row[0]})

    airports_dict = sorted(airports_dict.items())
    destination_ident = airports_dict[-1][1]
    return destination_ident


def game_info():
    print("\n\nThe world is not what it used to be. A virus has infected most of the population, "
          "turning people into zombies.\n"
          "At your destination airport there is rumored to be a vaccine.\nYou must get there to survive this nightmare.\n")
    time.sleep(5)
    print("This game uses turn-based combat. The player attacks first and then each enemy attacks the player.\n"
          "If your health during combat decreases to zero, you die. Pay attention to your statistics.")
    print("You gain experience points for defeating enemies. With enough points you level up and your damage and health increases.\n")
    time.sleep(5)
    print("You need fuel in order to travel to another airport. You can search for more fuel and bandages at each airport.\n")
    time.sleep(4)


def display_player_stats(screen_name):
    player_stats = search_db(f"SELECT player_lvl, experience, player_health, bandage, kerosene FROM player, inventory WHERE inventory.inventory_id = player.inventory_id AND screen_name = '{screen_name}'")
    player_lvl, exp, player_hp, bandage, fuel = player_stats[0][0], player_stats[0][1], player_stats[0][2], player_stats[0][3], player_stats[0][4]
    if player_lvl == 1:
        max_exp = 10
        max_hp = 100
    elif player_lvl == 2:
        max_exp = 20
        max_hp = 150
    else:
        max_exp = "UNLIMITED"
        max_hp = 200
    print(f"{Fore.GREEN}LVL. {player_lvl}   EXP: {exp}/{max_exp}   HP: {player_hp}/{max_hp}  BANDAGES: {bandage}  FUEL: {fuel}")


def player_continue(screen_name,location):
    is_searched = False
    current_airport = search_db(f"SELECT airport.name FROM airport WHERE ident = '{location}'")[0][0]
    destination_airport = search_db(f"SELECT airport.name FROM airport, player WHERE screen_name = '{screen_name}' AND destination = ident")[0][0]

    while True:
        print(f"Your current location is {current_airport}. Your destination is {destination_airport}.")
        display_player_stats(screen_name)
        print("\n   1. Search the airport\n   2. Travel\n   3. Check game info")
        answer = input("\nChoose your action (1-3): ")
        choice = input_check(answer,3)
        if choice == 1:
            if is_searched:
                print("\nYou have already searched the airport.")
            else:
                search_airport(screen_name)
                is_searched = True
        elif choice == 2:
            airport_list, screen_name = travel_choice(screen_name, location)
            break
        elif choice == 3:
            game_info()

    return airport_list, screen_name

