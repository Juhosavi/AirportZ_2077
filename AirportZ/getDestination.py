from flask import Blueprint, request, jsonify
from connection import get_connection
from search_db import search_db

get_destination_bp = Blueprint('get_destination', __name__)


@get_destination_bp.route('/getDestination', methods=['GET'])
def get_destination():
    screen_name = request.args.get('name')
    destination_code, destination_name = get_destination_icao(screen_name)

    dest = {
        'destination': destination_code,
        'destination_name': destination_name
    }
    return jsonify(dest), 200


def get_destination_icao(screen_name):
    dest = (search_db(f"SELECT destination FROM player WHERE screen_name = '{screen_name}'")[0][0])
    dest_name = (search_db(f"SELECT name FROM airport WHERE airport.ident = '{dest}'")[0][0])
    return dest, dest_name
