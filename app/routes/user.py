from datetime import datetime, timezone
from flask import Blueprint, request, jsonify, session
from app.models.user import User
from ..middleware import login_required

agent_bp = Blueprint('agent', __name__)

@agent_bp.route('/api/agents/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    type = 'agent' if 'agent' in request.path else 'client'
    User.create_user(email, type)
    user = User.get_by_email(email)

    session['email'] = user['email']
    session['type'] = user['type']
    session['last_activity'] = datetime.now(timezone.utc).isoformat()
    return jsonify({'status': 'success', 'email': email, 'type': 'type'})

@agent_bp.route('/api/agent/logout', methods=['GET'])
def logout():
    session.clear()
    return jsonify({'status': 'success', 'message': 'Logged out successfully'})

@agent_bp.route('/api/agents/conversations', methods=['GET'])
@login_required
def get_conversations():
    from app import db
    conversations = db.messages.find(
        {"email": session['email']},
    ).sort("created_at", -1).limit(20)

    return jsonify({
        'status': 'success',
        'data': list(conversations)
    })