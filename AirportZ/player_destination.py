from flask import Blueprint, request, jsonify
from connection import get_connection
from geopy.distance import geodesic

player_destination_bp = Blueprint('player_destination', __name__)
yhteys = get_connection()

@player_destination_bp.route('/playerdestination', methods=['GET'])
def player_destination():
    location_ident = request.args.get('ident')
    yhteys = get_connection()
    cursor = yhteys.cursor()

    cursor.execute("SELECT latitude_deg, longitude_deg FROM airport WHERE ident = %s", (location_ident,))
    location1 = cursor.fetchone()
    cursor.close()

    if not location1:
        return jsonify({'error': 'Invalid airport identifier'}), 404

    cursor = yhteys.cursor()
    cursor.execute("SELECT country.name FROM country JOIN airport ON country.iso_country = airport.iso_country WHERE airport.ident = %s", (location_ident,))
    country = cursor.fetchone()[0]
    cursor.close()

    cursor = yhteys.cursor()
    cursor.execute("SELECT ident, latitude_deg, longitude_deg FROM airport JOIN country ON airport.iso_country = country.iso_country WHERE country.name = %s AND ident != %s", (country, location_ident))
    airports = cursor.fetchall()
    cursor.close()

    airports_dict = {}
    for ident, lat, lng in airports:
        location2 = (lat, lng)
        distance = round(geodesic(location1, location2).km, 3)
        airports_dict[distance] = ident

    if airports_dict:
        max_distance = max(airports_dict)
        destination_ident = airports_dict[max_distance]
        return jsonify({'farthest_airport_ident': destination_ident}), 200
    else:
        return jsonify({'error': 'No other airports found in the same country'}), 404
