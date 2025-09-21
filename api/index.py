from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Simple in-memory data
users = [
    {"id": 1, "username": "sunita", "password": "password123", "role": "parent"},
    {"id": 2, "username": "ananya", "password": "password123", "role": "child", "parent_id": 1},
    {"id": 3, "username": "ishaan", "password": "password123", "role": "child", "parent_id": 1},
]

notes = [
    {"id": 1, "title": "Math Homework", "content": "Complete chapter 5", "owner_id": 2},
    {"id": 2, "title": "Science Project", "content": "Research plants", "owner_id": 2},
    {"id": 3, "title": "Art Class", "content": "Paint landscape", "owner_id": 3},
]

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/')
def home():
    return {"message": "NoteNext API"}

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = next((u for u in users if u["username"] == data["username"] and u["password"] == data["password"]), None)
    if user:
        return {"access_token": user["username"], "user": {"id": user["id"], "username": user["username"], "role": user["role"]}}
    return {"error": "Invalid"}, 400

@app.route('/signup', methods=['POST'])
def signup():
    return {"message": "User created"}

@app.route('/available-children')
def available_children():
    return []

@app.route('/children')
def children():
    token = request.args.get('token')
    if token == "sunita":
        return [{"id": 2, "username": "ananya"}, {"id": 3, "username": "ishaan"}]
    return []

@app.route('/notes')
def get_notes():
    token = request.args.get('token')
    child_id = request.args.get('child_id', type=int)
    
    if token == "sunita":
        if child_id:
            return [n for n in notes if n["owner_id"] == child_id]
        return notes
    elif token == "ananya":
        return [n for n in notes if n["owner_id"] == 2]
    elif token == "ishaan":
        return [n for n in notes if n["owner_id"] == 3]
    return []

@app.route('/notes', methods=['POST'])
def create_note():
    return {"id": 4, "title": "New Note", "content": "Content"}

@app.route('/folders')
def folders():
    return []

if __name__ == '__main__':
    app.run()