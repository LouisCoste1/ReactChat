from flask import Blueprint, request, jsonify, session
import sqlite3
from cryptography.fernet import Fernet
import os

note_routes = Blueprint('notes', __name__)

key = os.getenv('ENCRYPTION_KEY')
if key == None:
    print("WARNING. NOT KEY IS SET FOR ENCRYPTION")
    key = "AbwwULkEnfd_ivXPkoaLJtIJUPe1kHapYjkQQ1NXnKY=".encode()
cipher_suite = Fernet(key)

def encrypt(data):
    return cipher_suite.encrypt(data.encode()).decode()

def decrypt(data):
    return cipher_suite.decrypt(data.encode()).decode()

@note_routes.route('/create', methods=['POST'])
def create_note():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"msg": "Unauthorized"}), 401
    
    data = request.get_json()
    encrypted_content = encrypt(data['content'])
    conn = sqlite3.connect('database/app.db')
    c = conn.cursor()
    c.execute('INSERT INTO notes (user_id, content, title) VALUES (?, ?, ?)', 
              (user_id, encrypted_content, data["title"]))
    newnoteid = c.lastrowid
    conn.commit()
    conn.close()
    return jsonify({"msg": "Note created", "id_created": newnoteid}), 201

@note_routes.route('/', methods=['GET'])
def get_notes():
    """ Return all the notes that the user has"""
    
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"msg": "Unauthorized"}), 401
    
    conn = sqlite3.connect('database/app.db')
    c = conn.cursor()
    c.execute('SELECT id, content, title FROM notes WHERE user_id = ?', (user_id,))
    notes = c.fetchall()
    conn.close()
    return jsonify(notes=[{"id": note[0], "content": decrypt(note[1]), "title": note[2]} for note in notes]), 200
    



@note_routes.route('/note', methods=["GET"])
def get_note():
    """ Return the note the user asked for (if he has it)"""

    user_id = session.get('user_id')
    note_id = request.args.get("note_id")
    if not user_id or not note_id:
        return jsonify({"msg": "Unauthorized"}), 401
    
    conn = sqlite3.connect('database/app.db')
    c = conn.cursor()
    c.execute('SELECT id, content FROM notes WHERE user_id = ? AND id = ?', (user_id, note_id))
    note = c.fetchone()
    if note == None:
        return jsonify(notes={"id": -1, "content": "", "err": True, "msg": "note doesn't exists"})
    conn.close()
    return jsonify(notes={"id": note[0], "content": decrypt(note[1])}), 200



@note_routes.route('/note', methods=["DELETE"])
def delete():
    """ Return the note the user asked for (if he has it)"""

    user_id = session.get('user_id')
    note_id = request.args.get("note_id")
    if not user_id or not note_id:
        return jsonify({"msg": "Unauthorized"}), 401
    
    try:
        conn = sqlite3.connect('database/app.db')
        c = conn.cursor()
        c.execute('DELETE FROM notes WHERE user_id = ? AND id = ?', (user_id, note_id))
        conn.commit()
        
        if c.rowcount == 0:
            return jsonify({"msg": "Unauthorized or note does not exist"}), 403
       
        return jsonify({"msg": "note deleted"}), 200
    except Exception as e:
        print(e)
        conn.rollback()
        return jsonify({"msg": f"an error occured"}), 500

    finally:
        conn.close()


@note_routes.route("/note", methods=["PUT"])
def update_note():
    """update and existing note"""

    user_id = session.get("user_id")
    data = request.get_json()
    encrypted_content = encrypt(data['content'])
    conn = sqlite3.connect('database/app.db')
    c = conn.cursor()
    c.execute('UPDATE  notes SET content = ?, title = ? WHERE id = ? AND user_id = ?', 
              (encrypted_content, data['title'], data["id"], user_id))
    conn.commit()
    conn.close()
    if c.rowcount == 0:
            return jsonify({"msg": "Unauthorized"}), 403
    return jsonify({"msg": "Note updated"}), 201