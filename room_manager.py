from random import randint

CHARS = '123456789ABCDEF'

def generate_room_number():
    return ''.join([CHARS[randint(0, len(CHARS)-1)] for _ in range(4)])


room = {
    'code': 'A2CF',
    'members': [
        {
            'username': 'Azure',
            'location': 'location data',
            'can_see': ['silver'],
            'role': 'editor'
        },
        {
            'username': 'silver',
            'location': 'location data',
            'can_see': ['Azure'],
            'role': 'guest'
        },
        {
            'username': 'Pitou',
            'location': 'location data',
            'can_see': ['Azure'],
            'role': 'guest'
        },
        {
            'username': 'Arthur',
            'location': 'location data',
            'can_see': ['silver'],
            'role': 'guest'
        }
    ],
    'map': ... # a polygon
}