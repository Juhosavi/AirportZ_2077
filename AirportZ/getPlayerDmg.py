from flask import Blueprint, request, jsonify
from search_db import search_db


get_player_dmg_bp = Blueprint('get_player_dmg', __name__)


@get_player_dmg_bp.route('/getPlayerDmg', methods=['GET'])
def get_player_dmg():
    lvl = request.args.get('name')
    min_dmg, max_dmg = players_dmg(lvl)

    player_dmg = {
        'min_dmg': min_dmg,
        'max_dmg': max_dmg
    }
    return jsonify(player_dmg), 200


def players_dmg(lvl):
    result = search_db(f"SELECT min_dmg, max_dmg FROM player_dmg WHERE player_dmg.player_lvl = '{lvl}'")
    min_dmg, max_dmg = result[0][0], result[0][1]
    return min_dmg, max_dmg
