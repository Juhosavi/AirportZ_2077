from flask import Blueprint, request, jsonify
from search_db import search_db


get_enemy_stats_bp = Blueprint('get_enemy_stats', __name__)


@get_enemy_stats_bp.route('/getEnemyStats', methods=['GET'])
def get_enemy_stats():
    icao = request.args.get('name')
    enemy_lvl, enemy_hp, min_dmg, max_dmg, exp = get_enemies(icao)

    enemy_stats = {
        'enemy_lvl': enemy_lvl,
        'enemy_hp': enemy_hp,
        'min_dmg': min_dmg,
        'max_dmg': max_dmg,
        'exper': exp
    }
    return jsonify(enemy_stats), 200


def get_enemies(new_location):
    result = search_db(f"SELECT enemy_lvl, enemy_health, enemy_MINdmg, enemy_MAXdmg, exp_per_kill FROM enemy, airport WHERE airport.difficulty = enemy.enemy_lvl AND airport.ident = '{new_location}'")
    enemy_lvl, enemy_hp, mindmg, maxdmg, exp = result[0][0], result[0][1], result[0][2], result[0][3], result[0][4]
    return enemy_lvl, enemy_hp, mindmg, maxdmg, exp
