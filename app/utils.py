from itsdangerous import TimedSerializer, URLSafeSerializer
import jwt
import datetime
from dotenv import load_dotenv
from flask import current_app
from flask_mail import Message
import os

load_dotenv()

def generate_token(user_id):
    #Generate token for the user ID
    serializer = TimedSerializer(current_app.config['MAGIC_KEY'])

    return serializer.dumps({'user_id': user_id})

def send_magic_link(mail, email, magic_link):
    msg = Message("Magic link login", recipients=[email])
    msg.body = f"Here is your login link {magic_link}"
    mail.send(msg)

def generate_session_token(user_id):
    """ Generate a session token using user_id. """
    serializer = URLSafeSerializer(current_app.config['SUPER_SECRET_KEY'])
    return serializer.dumps({'user_id': user_id})

def encode_auth_token(user_id, super_secret_key):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1), #The expiration time of the token. In this case, it will expire in 1 day.
            'iat': datetime.datetime.utcnow(), #The time the token was issued.
            'sub': user_id # The subject of the token
        }
        return jwt.encode(
            payload,
            super_secret_key,
            algorithm='HS256'
        )
    except Exception as e:
        return str(e)
    
def decode_auth_token(auth_token, super_secret_key):
    try:
        payload = jwt.decode(auth_token, super_secret_key, algorithms=['HS256'])
        return payload['sub','super_secret_key']  # Return the user ID (or any other claim you're interested in)
    except jwt.ExpiredSignatureError:
        return 'Login token has expired'
    except jwt.InvalidTokenError:
        return 'Invalid token'
    
def validate_session_token(session_token):
    super_secret_key=current_app.config["SUPER_SECRET_KEY"]
    user_id = decode_auth_token(session_token, super_secret_key)

    if not user_id or isinstance(user_id, str) and "error" in user_id.lower():
        # token is invalid or has errors
        return None
    return user_id