from flask import Blueprint, request, jsonify
from connection import get_connection
from search_db import search_db

get_airport_levels_bp = Blueprint('get_airport_levels', __name__)


@get_airport_levels_bp.route('/getAirportLevels', methods=['GET'])
def get_airport_levels():
    airports = [request.args.get('airport1'), request.args.get('airport2'), request.args.get('airport3'),
                request.args.get('airport4'), request.args.get('airport5'), request.args.get('airport6')]
    levels = []

    i = 0
    while i < len(airports):
        levels.append(search_db(f"SELECT difficulty FROM airport WHERE airport.name = '{airports[i]}'")[0][0])
        i = i+1

    result = {
        'level1': levels[0],
        'level2': levels[1],
        'level3': levels[2],
        'level4': levels[3],
        'level5': levels[4],
        'level6': levels[5]
    }

    return jsonify(result), 200
