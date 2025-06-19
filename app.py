from flask import Flask, request, jsonify
from flask_cors import CORS
from random import randint

app = Flask(__name__)
CORS(app)
rooms = {}
CHARS = '123456789ABCDEF'
ATTRIBUTES = {'chat': {'one_per_user': False}, 'map': {'one_per_user': False}, 'location': {'one_per_user': True}}
DEFAULT_SETTINGS = { 
    'time_between_updates': 5
}

def generate_room_number():
    while True:
        code = ''.join([CHARS[randint(0, len(CHARS) - 1)] for _ in range(4)])
        if code not in rooms:
            return code

@app.route('/')
def home():
    return jsonify('hello, world!')

@app.route('/create', methods=['POST'])
def create_room():
    room_code = generate_room_number()
    rooms[room_code] = {
        attr: [] for attr in ATTRIBUTES.keys()
    }
    rooms[room_code]['members'] = {}
    rooms[room_code]['settings'] = {}
    return jsonify({'room_code': room_code})

@app.route('/join/<room_code>', methods=['POST'])
def join_room(room_code):
    data = request.json
    if room_code not in rooms:
        return jsonify({'error': 'Room not found'}), 404
    
    username = data['username']
    if len(rooms[room_code]['members']) == 0:
        rooms[room_code]['members'][username] = {   
            'role': 'host'
        }
    rooms[room_code]['members'][username] = {
        'role': 'guest'
    }
    return jsonify({'message': f'{username} joined room {room_code}.'})

@app.route('/room/<room_code>', methods=['POST'])
def send_info(room_code):
    data = request.json
    username = data.get('username')
    
    if room_code not in rooms:
        return jsonify({'error': f'Room {room_code} not found'}), 404
    
    if username not in rooms[room_code]['members']:
        return jsonify({'error': f'User {username} not found in room {room_code}'}), 404
    
    for attr in data:
        if attr not in ATTRIBUTES.keys():
            continue
        add_attribute(room_code, attr, username, data[attr])

    return jsonify({'message': f'{username} sent info.'})

@app.route('/room/<room_code>', methods=['GET'])
def get_info(room_code):
    if room_code not in rooms:
        return jsonify({'error': f'Room {room_code} not found'}), 404
    
    users = [user for user in rooms[room_code]['members'].keys()]
    data = {'users': users}
    for attr in ATTRIBUTES.keys():
        data[attr] = rooms[room_code][attr]
    return jsonify(data)


@app.route('/room/<room_code>/<attr>', methods=['GET'])
def get_attr(room_code, attr):
    if room_code not in rooms:
        return jsonify({'error': f'Room {room_code} not found'}), 404
    
    if attr not in ATTRIBUTES.keys():
        return jsonify({'error': f'Attribute: {attr} does not exist'}), 404
     
    users = [user for user in rooms[room_code]['members'].keys()]

    data = {'users': users}
    data[attr] = rooms[room_code][attr]
    return jsonify(data)


@app.route('/room/<room_code>/settings', methods=['POST'])
def update_settings(room_code):
    data = request.json
    username = data.get('username', None)

    if room_code not in rooms:
        return jsonify({'error': f'Room {room_code} not found'}), 404
    
    if username not in rooms[room_code]['members']:
        return jsonify({'error': f'User {username} not found in room {room_code}'}), 404
    
    if rooms[room_code]['members'][username]['role'] != 'host':
        return jsonify({'error': f'User {username} is not a host in room {room_code}'}), 403

    rooms[room_code]['settings'].update(data['settings'])
    return jsonify({'message': f'Settings updated for room {room_code}.'})



@app.route('/room/<room_code>/settings', methods=['GET'])
def get_settings(room_code):
    if room_code not in rooms:
        return jsonify({'error': f'Room {room_code} not found'}), 404
    
    return jsonify(rooms[room_code]['settings'])






@app.route('/room/<room_code>', methods=['DELETE'])
def leave_room(room_code):
    data = request.json
    username = data.get('username')

    if room_code not in rooms:
        return jsonify({'error': f'Room {room_code} not found'}), 404
    
    if username not in rooms[room_code]['members']:
        return jsonify({'error': f'User {username} not found in room {room_code}'}), 404
    
    del rooms[room_code]['members'][username]
    if not rooms[room_code]['members']:
        del rooms[room_code]
    return jsonify({'message': f'{username} left room {room_code}.'})

@app.route('/rooms', methods=['GET'])
def list_rooms():
    return jsonify({'rooms': list(rooms.keys())})





def add_attribute(room, attr, user, content):
    if room not in rooms:
        return jsonify({'error': f'Room {room} not found'}), 404
    
    if user not in rooms[room]['members']:
        return jsonify({'error': f'User {user} not found in room {room}'}), 404
    
    if ATTRIBUTES[attr]['one_per_user']:
        for item in rooms[room][attr]:
            if item['username'] == user:
                item =       {'username': user, 'content': content}
                return jsonify({'message': f'{user} updated {attr} in room {room}.'})

    rooms[room][attr].append({'username': user, 'content': content})
    return jsonify({'message': f'{user} added {attr} in room {room}.'})
