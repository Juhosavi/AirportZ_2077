from flask import Blueprint, request, jsonify
from connection import get_connection
from search_db import search_db

battle_victory_bp = Blueprint('battle_victory', __name__)


@battle_victory_bp.route('/battleVictory', methods=['GET'])
def battle_victory():
    screen_name = request.args.get('name')
    new_location = request.args.get('new_location')
    experience = request.args.get('experience')
    player_hp = request.args.get('player_hp')
    bandage = request.args.get('bandage')
    player_lvl = request.args.get('player_lvl')
    fuel = search_db(f"SELECT kerosene FROM inventory, player WHERE screen_name = '{screen_name}' AND player.inventory_id = inventory.inventory_id")[0][0]
    battles_won = search_db(f"SELECT battles_won FROM player WHERE screen_name = '{screen_name}'")[0][0]
    battles_won = battles_won + 1
    fuel = fuel - 1

    search_db(f"UPDATE inventory, player SET location = '{new_location}', kerosene = '{fuel}', experience = '{experience}', player_health = '{player_hp}', bandage = '{bandage}', player_lvl = '{player_lvl}', battles_won = '{battles_won}' WHERE screen_name = '{screen_name}' AND player.inventory_id = inventory.inventory_id")

    result = {'affirm': 'affirmative'
    }

    return jsonify(result), 200




# name, new_location, experience, player_hp, bandage, player_lvl
