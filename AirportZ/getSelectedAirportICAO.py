from flask import Blueprint, request, jsonify
from search_db import search_db

get_selected_airport_icao_bp = Blueprint('get_selected_airport_icao', __name__)


@get_selected_airport_icao_bp.route('/getSelectedAirportICAO', methods=['GET'])
def get_selected_airport_icao():
    airport_name = request.args.get('name')
    new_icao = get_selected_icao(airport_name)

    new_airport_icao = {
        'new_airport': new_icao
    }
    return jsonify(new_airport_icao), 200


def get_selected_icao(airport_name):
    icao = (search_db(f"SELECT ident FROM airport WHERE airport.name = '{airport_name}'")[0][0])
    return icao
