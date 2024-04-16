from flask import Flask, request, jsonify
import mysql.connector
from player_create import add_new_player, player_continue, player_destination, search_db, player_name_check, create_inventory, start_country
from flask_cors import CORS
from travel import travel_choice

app = Flask(__name__)
CORS(app, resources={r"/loadPlayer": {"origins": "http://localhost:63342"}})
CORS(app, resources={r"/addPlayer": {"origins": "http://localhost:63342"}})
app.config['CORS_HEADERS'] = 'Content-Type'

yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='testgame',
    user='root',
    password='mariacat123',
    autocommit=True
)

# Pelaajan lataaminen
@app.route('/loadPlayer', methods=['GET'])
def load_player():

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

@app.route('/addPlayer', methods=['POST'])
def flask_add_new_player():

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

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=3000)
