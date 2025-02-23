from datetime import datetime, timezone
from flask import Blueprint, request, jsonify, session
from flask_socketio import emit
from app import socketio
from ..config import Config
from ..services.ai import AIService
from ..models.message import Message
from ..middleware import login_required

chat_bp = Blueprint('chat', __name__)
ai_service = AIService()

@chat_bp.route('/api/conversations', methods=['POST'])
@login_required
def create_conversation():
    data = request.json
    content = data.get('content')
    content = data.get('content')
    sender_type = data.get('sender_type', 'client')
    conversation_id = datetime.now(timezone.utc)
    
    if not content:
        return jsonify({'error': 'Message content is required'}), 400
    Message.create(content, sender_type, conversation_id)
    session['last_activity'] = datetime.now(timezone.utc)
    return jsonify({'conversation_id': 'new_id'})

@chat_bp.route('/api/conversations/<conversation_id>/messages', methods=['GET'])
@login_required
def get_messages(conversation_id):
    messages = Message.get_conversation(conversation_id)
    return jsonify(messages)

@chat_bp.route('/', methods=['GET'])
def index():
    return jsonify({'message': Config.check_db()})

@socketio.on("connect")
def handle_connect():
    print("Client connected")

@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")

@socketio.on("message")
def handle_message(data):
    print(f"Received message: {data}")
    emit("message", {"text": data, "sender": "server"}, broadcast=True)