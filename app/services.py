from flask import Flask, jsonify, url_for, redirect
from app import db, mail
from app.models import User
from app.utils import generate_token, send_magic_link
from datetime import timedelta, datetime


def test():
    return jsonify({'Balls': 'check your mouth for them'}), 200

def authenticate(form):
    # Get email from form
    email = form.get('email')
    # Make sure inputs are valid
    if '@' not in email or '.' not in email.split('@')[1]:
        return jsonify({'error': 'Invalid email'}), 400
    
    #Check if user exists if the user does exist send magic link
    user = User.query.filter_by(email=email).first()
    if user:
        return user_login(user)
    
    #Create new user
    user = User(
        email=email,
        user_created = datetime.utcnow()
        )
    #Add new user to the database
    db.session.add(user)
    # Flush the session to generate an ID for the user
    db.session.flush()
    # Refresh the user object to get the assigned ID
    db.session.refresh(user) 
    # Generate a token and set it as the user's login token
    user.login_token = generate_token(user.id)
    # Set the token expiry time
    user.token_expiry = datetime.utcnow() + timedelta(minutes=10)
    # Set the user time created
    # user.user_created = datetime.utcnow()
    # Commit the changes to the database
    db.session.commit()

    # Send a magic link to the user's email
    email = user.email
    magic_link = url_for('magic_link', token=user.login_token, _external=True)
    send_magic_link(mail, email, magic_link)

    return jsonify({'message': 'Signup successful, check your email for a magic link'}), 200

def user_login(user):
    #Extract email form user
    email = user.email
    #Generate new token for user login
    user.login_token = generate_token(user.id)
    # Set the token expiry time
    user.token_expiry = datetime.utcnow() + timedelta(minutes=10)
    # Save the updated user to the database
    db.session.commit()
    # Send a magic link to the user's email
    magic_link = url_for('magic_link', token=user.login_token, _external=True)
    send_magic_link(mail, email, magic_link)

    return jsonify({'message': 'Login successful, check your email for a magic link'}), 200

def verify_user(token):
    # Find a user with this token
    user = User.query.filter_by(login_token=token).first()
    if not user:
        return jsonify({'error': 'Invalid or expired token'}), 400
    
    # Check if the token has expired
    if datetime.utcnow() > user.token_expiry:
        return jsonify({'error': 'Expired token'}), 400

    # Mark the user as authenticated
    user.authenticated = True

    # Clear the user's login token
    user.login_token = None

    # Save the updated user to the database
    db.session.commit()

    return jsonify({'message': 'User authenticated successfully'}), 200

def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('signup'))
