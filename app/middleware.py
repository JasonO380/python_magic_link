from functools import wraps
from flask import request, jsonify
from app.utils import validate_session_token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Check if the token is in the header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].replace("Bearer", "")

        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        user_id = validate_session_token(token)
        if not user_id:
            return jsonify({"message": "Token is invalid or expired"}), 401
        return f(user_id, *args, **kwargs) # forward user_id to the actual function
    return decorated