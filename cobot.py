import json
import requests

# Configuration
# -------------

GITHUB_TOKEN = ''
GITTER_TOKEN = ''

ROOMS = [
    'coala/coala',
    'coala/cobot-test'
]

# Functionality
# -------------

def get_room_ids(rooms):
    """
    :pararm rooms:
        List of room names whose room id has to be retreived.
    :return:
        A list of room ids.
    """

    ids = dict()
    for room in rooms:
        rq = requests.get("https://api.gitter.im/v1/rooms?q={room_name}".format(roon_name=room), headers={"Authorization": "Bearer {token}".format(token=GITTER_TOKEN)})
        response = json.loads(rq.json())
        for i in response:
            ids[i.name] = i.id
    return ids