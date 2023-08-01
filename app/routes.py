from app.services import test 
from app import app
from flask import request, jsonify, url_for, render_template
from app.models import User
from app.services import user_login, authenticate, verify_user, delete_user

@app.route('/authenticate', methods=['POST', 'GET'])
def authorize():
    #if the method is POST the form data gets inout into the db
    #if the method is GET we retrieve the sign up HTML
    if request.method == 'POST':
        return authenticate(request.form)
    users = User.query.all()
    return render_template('sign_up.html', users=users)

@app.route('/login', methods=['POST'])
def login():
    #Check to see if user exists in the login route instead of services.py
    email = request.form.get("email")
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return user_login(request.get_json())

@app.route('/magic-link/<token>')
def magic_link(token):
    """Handles user authentication when a magic link is clicked."""

    return verify_user(token)

@app.route('/delete_user', methods=['POST'])
def delete():
    user_id = request.form.get('user_id')
    return delete_user(user_id)