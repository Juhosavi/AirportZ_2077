import connection
from flask import Blueprint, request, jsonify
from connection import get_connection

load_player_bp = Blueprint('load_player', __name__)
yhteys = get_connection()


@load_player_bp.route('/loadPlayer', methods=['GET'])
def load_player():
    yhteys = connection.get_connection()
    pelaajan_nimi = request.args.get('name')
    kursori = yhteys.cursor()
    kursori.execute("SELECT id, screen_name, location FROM player WHERE screen_name = %s", (pelaajan_nimi,))
    tulos = kursori.fetchone()
    kursori.close()

    if tulos:
        pelaajan_data = {
            'id': tulos[0],
            'screen_name': tulos[1],
            'location': tulos[2]
        }
        return jsonify(pelaajan_data), 200
    else:
        pelaajan_data = {'virhe': 'Pelaajaa ei löydy'}
        return jsonify(pelaajan_data), 200
