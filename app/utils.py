from itsdangerous import TimedSerializer
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