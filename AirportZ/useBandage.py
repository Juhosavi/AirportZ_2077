from flask import Blueprint, request, jsonify
from connection import get_connection
from search_db import search_db

use_bandage_bp = Blueprint('use_bandage', __name__)


@use_bandage_bp.route('/useBandage', methods=['GET'])
def use_bandage():
    screen_name = request.args.get('name')
    bandage = search_db(f"SELECT bandage FROM inventory, player WHERE inventory.inventory_id = player.inventory_id AND screen_name = '{screen_name}'")[0][0]
    bandage = bandage - 1
    search_db(f"UPDATE inventory, player SET bandage = '{bandage}' WHERE inventory.inventory_id = player.inventory_id AND screen_name = '{screen_name}'")
    #tän pitää palauttaa jotain. Tee sit viel et hela nousee myös 50 pojoo btw

    bndg = {
        'test': 0
    }
    return jsonify(bndg), 200
