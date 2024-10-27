from flask import Blueprint, request, make_response, jsonify, session
from flask_bcrypt import Bcrypt
import sqlite3

user_routes = Blueprint('users', __name__)
bcrypt = Bcrypt()

@user_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    conn = sqlite3.connect('database/app.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)', 
                  (data['username'], data["email"], hashed_password))
        conn.commit()
        return jsonify({"msg": "User registered"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"msg": "User already exists"}), 400
    finally:
        conn.close()

@user_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    conn = sqlite3.connect('database/app.db')
    c = conn.cursor()
    c.execute('SELECT id, password_hash FROM users WHERE username = ? OR email = ?', (data['username'], data['username']))
    user = c.fetchone()
    if user and bcrypt.check_password_hash(user[1], data['password']):
        response = make_response({"msg": "Logged in"})
        session['user_id'] = user[0]

        return response
    return jsonify({"msg": "Bad username or password"}), 401

@user_routes.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    return jsonify({"msg": "Logged out successfully"}), 200

@user_routes.route('/delete', methods=['DELETE'])
def delete():
    username_to_delete = request.args.get("username")
    request_user_id = session.get("user_id")

    if not username_to_delete or not request_user_id:
        return jsonify({"msg": "Missing username or user_id"}), 400

    try:
        conn = sqlite3.connect('database/app.db')
        c = conn.cursor()
        c.execute('DELETE FROM users WHERE username = ? AND id = ?', (username_to_delete, request_user_id))
        conn.commit()

        if c.rowcount == 0:
            return jsonify({"msg": "Unauthorized or user does not exist"}), 403

        session.pop("user_id", None)
        return jsonify({"msg": "User deleted successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"msg": f"an error occured"}), 500

    finally:
        conn.close()
