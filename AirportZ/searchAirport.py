import random
from flask import Blueprint, request, jsonify
from connection import get_connection
from search_db import search_db

search_airport_bp = Blueprint('search_airport', __name__)


@search_airport_bp.route('/searchAirport', methods=['GET'])
def search_airport():
    screen_name = request.args.get('name')
    bandage, fuel = search_airport_items(screen_name)

    found_items = {
        'bandage': bandage,
        'fuel': fuel
    }
    return jsonify(found_items), 200


def search_airport_items(screen_name):
    result = search_db(f"SELECT bandage, kerosene FROM inventory, player WHERE screen_name = '{screen_name}' AND player.inventory_id = inventory.inventory_id")
    bandage = random.randint(0,2)
    kerosene = random.randint(1,2)
    # print(f"You found {bandage} bandage!")
    # print(f"You found {kerosene} fuel!\n")
    new_bandage = result[0][0] + bandage
    new_kerosene = result[0][1] + kerosene
    sql = f"UPDATE inventory, player SET bandage = '{new_bandage}', kerosene = '{new_kerosene}' WHERE screen_name = '{screen_name}' AND player.inventory_id = inventory.inventory_id"
    search_db(sql)
    return bandage, kerosene
