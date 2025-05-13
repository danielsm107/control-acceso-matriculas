from flask import Flask
from flask_socketio import SocketIO
from flask_login import LoginManager
from routes import main, admin, matriculas, api, auth

app = Flask(__name__)
app.secret_key = "clave_segura"
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

socketio = SocketIO(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = None
login_manager.init_app(app)

# Registro de Blueprints
app.register_blueprint(auth.auth)
app.register_blueprint(main.main)
app.register_blueprint(admin.admin)
app.register_blueprint(matriculas.matriculas)
app.register_blueprint(api.api)

# Loader de usuarios
from utils.db_utils import load_user
login_manager.user_loader(load_user)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
