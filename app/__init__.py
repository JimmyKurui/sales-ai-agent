from flask import Flask
from flask_session import Session
from flask_socketio import SocketIO
from flask_cors import CORS
from .config import Config

socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    Config.check_db()
    CORS(app)
    Session(app)
    socketio.init_app(app, cors_allowed_origins="*")
    
    from .routes import chat, user 
    app.register_blueprint(chat.chat_bp)
    app.register_blueprint(user.agent_bp)
    
    return app