# Python Magic Authentication

Python Magic Authentication is a Flask application that implements passwordless authentication via "magic links". Users sign up or log in by entering their email address, and a magic link is sent to their email. By clicking the link, users are authenticated.

## Application Flow

1. User submits their email via the `/authenticate` route.
2. If the user does not exist, a new user entry is created in the database. Whether the user is new or existing, a magic link is generated and sent to the user's email.
3. The user clicks the magic link in their email, which routes them to `/magic-link/<token>`. The token is verified, and if valid and not expired, the user is marked as authenticated in the database.

## Code Structure

### `app/models.py`

This file defines the User model for SQLAlchemy, which maps to the `user` table in the PostgreSQL database. Each user has an email, a profile (optional), a login token and its expiry time, a flag indicating whether they are authenticated, and timestamps for when the user was created and updated.

### `app/services.py`

This file defines the main business logic for handling user authentication.

- `authenticate(form)` handles the POST request to `/authenticate`, creating a new user if necessary, generating a login token, and sending the magic link.
- `user_login(user)` is called to handle the actual login, generating a new token, updating the expiry time, and sending the magic link.
- `verify_user(token)` handles the GET request to `/magic-link/<token>`, verifying the token and marking the user as authenticated.
- `delete_user(user_id)` handles the POST request to `/delete_user`, deleting the specified user.

### `app/routes.py`

This file defines the routes that the Flask application responds to, as well as the HTTP methods (GET, POST) that they respond to.

### `config.py`

This file defines the application configurations. It includes the base `Config` class, and two subclasses `DevelopmentConfig` and `ProductionConfig` for development and production settings respectively. The active config is determined by the `FLASK_ENV` environment variable. If `FLASK_ENV` is set to "production", the `ProductionConfig` will be used; if it's set to anything else or not set at all, the `DevelopmentConfig` will be used.

## Database Connection

The connection to the PostgreSQL database is made in the `create_app` function in `app/__init__.py`, where the SQLAlchemy object `db` is initialized with the application. The database URL is specified in the `SQLALCHEMY_DATABASE_URI` setting of the active configuration.

## Migrations

Database migrations are managed with Flask-Migrate, a Flask extension that handles SQLAlchemy database migrations. Migrations scripts are stored in the `migrations` directory. The commands `flask db migrate` and `flask db upgrade` are used to apply the migrations.
