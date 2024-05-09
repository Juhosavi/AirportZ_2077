from flask import Flask
from flask_cors import CORS
# from AirportZ.player_destination import player_destination_bp
from loadPlayer import load_player_bp
from addPlayer import add_player_bp
from displayStats import player_stats_bp
from getCloseAirports import close_airports_bp
from searchAirport import search_airport_bp
from getCoordinates import get_coordinates_bp
from getDestination import get_destination_bp
from useBandage import use_bandage_bp
from updateHealth import update_health_bp
from getSelectedAirportICAO import get_selected_airport_icao_bp
from getEnemyStats import get_enemy_stats_bp
from getPlayerDmg import get_player_dmg_bp
from battleVictory import battle_victory_bp
from getAirportLevels import get_airport_levels_bp

app = Flask(__name__)
CORS(app, resources={r"/loadPlayer": {"origins": "http://localhost:63342"}})
CORS(app, resources={r"/addPlayer": {"origins": "http://localhost:63342"}})
# CORS(app, resources={r"/playerdestination": {"origins": "http://localhost:63342"}})
CORS(app, resources={r"/displayStats": {"origins": "http://localhost:63342"}})
CORS(app, resources={r"/getCloseAirports": {"origins": "http://localhost:63342"}})
CORS(app, resources={r"/searchAirport": {"origins": "http://localhost:63342"}})
CORS(app, resources={r"/getCoordinates": {"origins": "http://localhost:63342"}})
CORS(app, resources={r"/getDestination": {"origins": "http://localhost:63342"}})
CORS(app, resources={r"/useBandage": {"origins": "http://localhost:63342"}})
CORS(app, resources={r"/updateHealth": {"origins": "http://localhost:63342"}})
CORS(app, resources={r"/getSelectedAirportICAO": {"origins": "http://localhost:63342"}})
CORS(app, resources={r"/getEnemyStats": {"origins": "http://localhost:63342"}})
CORS(app, resources={r"/getPlayerDmg": {"origins": "http://localhost:63342"}})
CORS(app, resources={r"/battleVictory": {"origins": "http://localhost:63342"}})
CORS(app, resources={r"/getAirportLevels": {"origins": "http://localhost:63342"}})
app.config['CORS_HEADERS'] = 'Content-Type'

app.register_blueprint(load_player_bp)
app.register_blueprint(add_player_bp)
# app.register_blueprint(player_destination_bp)
app.register_blueprint(player_stats_bp)
app.register_blueprint(close_airports_bp)
app.register_blueprint(search_airport_bp)
app.register_blueprint(get_coordinates_bp)
app.register_blueprint(get_destination_bp)
app.register_blueprint(use_bandage_bp)
app.register_blueprint(update_health_bp)
app.register_blueprint(get_selected_airport_icao_bp)
app.register_blueprint(get_enemy_stats_bp)
app.register_blueprint(get_player_dmg_bp)
app.register_blueprint(battle_victory_bp)
app.register_blueprint(get_airport_levels_bp)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=3000)

