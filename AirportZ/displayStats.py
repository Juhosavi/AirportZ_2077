from flask import Blueprint, request, jsonify
from connection import get_connection
from search_db import search_db
from player_create import display_player_stats

player_stats_bp = Blueprint('player_stats', __name__)
yhteys = get_connection()


@player_stats_bp.route('/displayStats', methods=['GET'])
def player_stats():
    player_name = request.args.get('name')
    kursori = yhteys.cursor()
    kursori.execute(f"SELECT player_lvl, experience, player_health, bandage, kerosene, destination, battles_won FROM player, inventory WHERE inventory.inventory_id = player.inventory_id AND screen_name = '{player_name}'")
    tulos = kursori.fetchone()
    kursori.close()

    if tulos[0] == 1:
        max_exp = 10
        max_hp = 100
    elif tulos[0] == 2:
        max_exp = 20
        max_hp = 150
    else:
        max_exp = "UNLIMITED"
        max_hp = 200

    if tulos:
        curr_player_stats = {
            'player_lvl': tulos[0],
            'experience': tulos[1],
            'player_health': tulos[2],
            'bandage': tulos[3],
            'kerosene': tulos[4],
            'max_exp': max_exp,
            'max_hp': max_hp,
            'destination': tulos[5],
            'battles_won': tulos[6]
        }
        return jsonify(curr_player_stats), 200
    else:
        curr_player_stats = {'virhe': 'Pelaajaa ei löydy'}
        return jsonify(curr_player_stats), 200


# def display_player_stats(screen_name):
#     player_stats = search_db(f"SELECT player_lvl, experience, player_health, bandage, kerosene FROM player, inventory WHERE inventory.inventory_id = player.inventory_id AND screen_name = '{screen_name}'")
#     player_lvl, exp, player_hp, bandage, fuel = player_stats[0][0], player_stats[0][1], player_stats[0][2], player_stats[0][3], player_stats[0][4]
#     if player_lvl == 1:
#         max_exp = 10
#         max_hp = 100
#     elif player_lvl == 2:
#         max_exp = 20
#         max_hp = 150
#     else:
#         max_exp = "UNLIMITED"
#         max_hp = 200
#     # print(f"{Fore.GREEN}LVL. {player_lvl}   EXP: {exp}/{max_exp}   HP: {player_hp}/{max_hp}  BANDAGES: {bandage}  FUEL: {fuel}")
#     return player_lvl, exp, player_hp, max_exp, max_hp, bandage, fuel
