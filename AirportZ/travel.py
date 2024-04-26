import colorama
from search_db import search_db
from geopy.distance import geodesic
import player_create
from input_validation import  input_check
from colorama import Fore, Back, Style
colorama.init(autoreset=True)


def get_levels(travel_list):
    i = 0
    level_list = []
    while i < len(travel_list):
        level_list.append(search_db(f"SELECT difficulty FROM airport WHERE airport.name = '{travel_list[i]}'")[0][0])
        i = i + 1

    return level_list


def get_airport_dictionary(location_ident):
    sql = f"SELECT latitude_deg, longitude_deg FROM airport WHERE airport.ident = '{location_ident}'"
    location1 = search_db(sql)
    sql = f"SELECT country.name FROM country, airport WHERE country.iso_country = airport.iso_country and airport.ident = '{location_ident}'"
    country = search_db(sql)[0][0]
    sql = f"SELECT airport.name, latitude_deg, longitude_deg FROM airport, country WHERE airport.iso_country = country.iso_country AND country.name = '{country}' AND airport.ident != '{location_ident}'"
    airports = search_db(sql)
    airports_dict = {}

    for row in airports:
        location2 = row[1], row[2]
        airports_dict.update({round(geodesic(location1, location2).km, 3): row[0]})

    airports_dict = sorted(airports_dict.items())
    return airports_dict


def three_closest_airports(airports_dict):
    three_airports = [airports_dict[0][1], airports_dict[1][1], airports_dict[2][1]]
    levels = get_levels(three_airports)
    counter = 0

    while counter < 3:
        print(f"{counter + 1}. {three_airports[counter]} - LVL {levels[counter]}")
        counter = counter + 1
    return three_airports


def nine_closest_airports(airports_dict):
    nine_airports = []
    counter = 0

    for i in range(0, 9):
        nine_airports.append(airports_dict[i][1])
    levels = get_levels(nine_airports)

    while counter < 9:
        print(f"{counter + 1}. {nine_airports[counter]} - LVL {levels[counter]}")
        counter = counter + 1
    return nine_airports


def travel_choice(screen_name, location_ident):
    airports_dict = get_airport_dictionary(location_ident)
    sql = f"SELECT kerosene FROM inventory, player WHERE inventory.inventory_id = player.inventory_id AND player.screen_name = '{screen_name}'"
    fuel = search_db(sql)[0][0]
    print("\n")

    if fuel < 1:
        print(f"{Fore.RED}You have no fuel. Search the airport to find some more.\n")
        return player_create.player_continue(screen_name, location_ident)
    elif fuel == 1:
        three_airports = three_closest_airports(airports_dict)
        return three_airports, screen_name
    elif fuel > 1:
        nine_airports = nine_closest_airports(airports_dict)
        return nine_airports, screen_name


def where_to_travel(travel_list, screen_name):
    choice = input("\nEnter airport number: ")
    choice = input_check(choice, len(travel_list))
    choice = choice-1
    selected_airport = travel_list[choice]
    print(f"\nYou have selected to travel to: {selected_airport}")
    sql = f"SELECT ident FROM airport WHERE airport.name = '{selected_airport}'"
    airport_ident = search_db(sql)[0][0]
    fuel_count(travel_list, screen_name)
    return airport_ident, screen_name

def fuel_count(travel_list, screen_name):
    fuel = search_db(f"SELECT kerosene FROM inventory, player WHERE inventory.inventory_id = player.inventory_id AND player.screen_name = '{screen_name}'")[0][0]
    if len(travel_list) < 4:
        fuel = fuel - 1
        sql = f"UPDATE inventory, player SET kerosene = '{fuel}' WHERE inventory.inventory_id = player.inventory_id AND player.screen_name = '{screen_name}'"
        search_db(sql)
    else:
        fuel = fuel - 2
        sql = f"UPDATE inventory, player SET kerosene = '{fuel}' WHERE inventory.inventory_id = player.inventory_id AND player.screen_name = '{screen_name}'"
        search_db(sql)


