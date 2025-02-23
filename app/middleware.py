
import jsonify
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import session
from .models.user import SESSION_TIMEOUT
# ---------------------- AUTH MIDDLEWARE ---------------------- #
def login_required(f):
    """Decorator to ensure user is authenticated and session is active."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session or 'last_activity' not in session:
            return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
        
        last_activity = datetime.fromisoformat(session['last_activity'])
        now = datetime.now(timezone.utc)

        if (now - last_activity) > timedelta(minutes=SESSION_TIMEOUT):
            session.clear()
            return jsonify({'status': 'error', 'message': 'Session expired, please log in again'}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function