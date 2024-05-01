from flask import Blueprint, request, jsonify
from connection import get_connection
from search_db import search_db

update_health_bp = Blueprint('update_health', __name__)


@update_health_bp.route('/updateHealth', methods=['GET'])
def update_health():
    screen_name = request.args.get('name')
    lvl = get_player_lvl(screen_name)
    hp = search_db(f"SELECT player_health FROM player WHERE screen_name = '{screen_name}'")[0][0]

    if lvl == 1:
        if hp >= 50:
            hp = 100
        elif hp < 50:
            hp = hp + 50
    elif lvl == 2:
        if hp >= 100:
            hp = 150
        elif hp < 100:
            hp = hp + 50
    elif lvl == 3:
        if hp >= 150:
            hp = 200
        elif hp < 150:
            hp = hp + 50

    search_db(f"UPDATE player SET player_health = '{hp}' WHERE screen_name = '{screen_name}'")

    hp_ret = {
        'test': 0
    }
    return jsonify(hp_ret), 200


def get_player_lvl(screen_name):
    lvl = search_db(f"SELECT player_lvl FROM player WHERE screen_name = '{screen_name}'")[0][0]
    return lvl
