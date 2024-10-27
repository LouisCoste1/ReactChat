from flask import Flask
from users import user_routes
from notes import note_routes

import os
from datetime import timedelta
from database.interface import init_db

app = Flask(__name__)
if os.getenv("flask_key", default="default") == "default":
	print("WARNING: NO SECRET KEY FOR USER SESSION")
app.secret_key = os.getenv("flask_key", default="default")
# app.config['SESSION_COOKIE_SECURE'] = True  # Cookies are only sent over HTTPS
# cannot use this on dev but should on prod
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevents JavaScript access to the session cookie


# Register blueprints for user and note routes
app.register_blueprint(user_routes, url_prefix='/users')
app.register_blueprint(note_routes, url_prefix='/notes')

if __name__ == '__main__':
	init_db()
	app.run(debug=True)