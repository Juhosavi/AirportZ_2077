from flask import Flask
from flask_cors import CORS
from loadPlayer import load_player_bp
from addPlayer import add_player_bp

app = Flask(__name__)
CORS(app, resources={r"/loadPlayer": {"origins": "http://localhost:63342"}})
CORS(app, resources={r"/addPlayer": {"origins": "http://localhost:63342"}})
app.config['CORS_HEADERS'] = 'Content-Type'

app.register_blueprint(load_player_bp)
app.register_blueprint(add_player_bp)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=3000)
