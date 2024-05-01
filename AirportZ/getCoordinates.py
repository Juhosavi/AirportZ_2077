from flask import Blueprint, request, jsonify
from connection import get_connection
from search_db import search_db

get_coordinates_bp = Blueprint('get_coordinates', __name__)


@get_coordinates_bp.route('/getCoordinates', methods=['GET'])
def get_coordinates():
    airport_ident = request.args.get('name')
    lat_long = get_airport_coords(airport_ident)

    coordinates = {
        'latitude': lat_long[0],
        'longitude': lat_long[1]
    }
    return jsonify(coordinates), 200


#tähän funktioon lähetetään icao-koodi, ja se palauttaa listan coords -> databasesta k.o. airportin latituden ja longituden indekseissä 1 ja 2
def get_airport_coords(airport_ident):
    coords = []

    for i in range(0, 6):
        coords.append(search_db(f"SELECT latitude_deg FROM airport WHERE airport.ident = '{airport_ident}'")[0][0])
        coords.append(search_db(f"SELECT longitude_deg FROM airport WHERE airport.ident = '{airport_ident}'")[0][0])

    return coords

