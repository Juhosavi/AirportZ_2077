from flask import Blueprint, request, jsonify
from player_create import add_new_player, player_name_check, create_inventory, start_country
from connection import get_connection

add_player_bp = Blueprint('add_player', __name__)
yhteys = get_connection()


@add_player_bp.route('/addPlayer', methods=['POST'])
def add_player():
    data = request.get_json()
    if data and 'name' in data:
        pelaajan_nimi = data['name']
        pelaajan_nimi = player_name_check(pelaajan_nimi)
        varaston_id = create_inventory()
        sijainti_tunniste = start_country()
        vastaus = add_new_player(pelaajan_nimi, sijainti_tunniste, varaston_id, yhteys)

        if vastaus:  # Tarkista onko pelaajan luonti onnistunut
            return jsonify(vastaus), 201  # Pelaaja luotu
        else:
            return jsonify({'virhe': 'Pelaajan luominen epäonnistui'}), 500  # Sisäinen virhe

    else:
        return jsonify({'virhe': 'Virheellinen tai puuttuva nimi'}), 400  # Huono pyyntö