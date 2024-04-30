
from geopy.distance import geodesic
from flask import Blueprint, request, jsonify
from connection import get_connection
from search_db import search_db

close_airports_bp = Blueprint('close_airports', __name__)


@close_airports_bp.route('/getCloseAirports', methods=['GET'])
def close_airports():
    location = request.args.get('name')
    airports_dict = get_airport_dictionary(location)
    airport_list = get_airport_list(airports_dict)

    ordered_airports = {
        'airport1': airport_list[0],
        'airport2': airport_list[1],
        'airport3': airport_list[2],
        'airport4': airport_list[3],
        'airport5': airport_list[4],
        'airport6': airport_list[5]
    }
    return jsonify(ordered_airports), 200



def get_airport_list(airports_dict):
    airport_list = []
    airport_list2 = []
    for airport in airports_dict:
        airport_list.append(airport[1])
    i = 0
    while i < 6:
        airport_list2.append(airport_list[i])
        i = i + 1

    return airport_list2

# def get_airports_coords(airports_dict):
#     coords_dict = {}
#     latitudes = []
#     longitudes = []
#     for i in range(0, 6):
#         latitudes.append(search_db(f"SELECT latitude_deg FROM airport WHERE airport.name = '{airports_dict[i][1]}'")[0][0])
#         longitudes.append(search_db(f"SELECT longitude_deg FROM airport WHERE airport.name = '{airports_dict[i][1]}'")[0][0])
#
#     for u in range(0, 6):
#         coords_dict.update({latitudes[u]: longitudes[u]})
#
#     return coords_dict
# #palauttaa koodrinaatit latitude longitude toisen dictionaryn lentokentille


def get_airport_dictionary(location_ident):
    sql = f"SELECT latitude_deg, longitude_deg FROM airport WHERE airport.ident = '{location_ident}'"
    location1 = search_db(sql)
    sql = f"SELECT country.name FROM country, airport WHERE country.iso_country = airport.iso_country and airport.ident = '{location_ident}'"
    country = search_db(sql)[0][0]
    sql = f"SELECT airport.name, latitude_deg, longitude_deg FROM airport, country WHERE airport.iso_country = country.iso_country AND country.name = '{country}' AND airport.ident != '{location_ident}'"
    airports = search_db(sql)
    airports_dict = {}

    for row in airports:
        location2 = row[1], row[2]
        airports_dict.update({round(geodesic(location1, location2).km, 3): row[0]})

    airports_dict = sorted(airports_dict.items())
    return airports_dict
#palauttaa dictionaryn, jossa ekana on lentokentän distance ja tokana nimi, (järkätty lähimmästä kauimmaiseen)