import json
import requests
import re

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

handlers = dict()

def get_room_ids(rooms):
    """
    :pararm rooms:
        List of room names whose room id has to be retreived.
    :return:
        A list of room ids.
    """

    ids = dict()
    for room in rooms:
        rq = requests.get("https://api.gitter.im/v1/rooms?q={room_name}".format(roon_name=room),
                          headers={"Authorization": "Bearer {token}".format(token=GITTER_TOKEN)})
        response = json.loads(rq.json())
        for i in response.results:
            ids[i.name] = i.id
    return ids

def get_messages(id):
    """
    :param id:
        The room ``id`` whose messages have to be retreived via the streaming API.
    :returns:
        A **requests response** object of the keep-alive request for getting the messages.
    """

    return requests.get("https://stream.gitter.im/v1/rooms/{room_id}/chatMessagges".format(room_id=id),
                        stream=True,
                        headers={"Authorization": "Bearer {token}".format(token=GITTER_TOKEN)})

def listen(regex, handlers=handlers):
    """
    A decorator to add the decorating function as a handler of
    message matching given regex.
    """
    def wrap(func):
        handlers[regex] = func
        func()
    return wrap

def handle_messages(res):
    """
    Call the handlers if the message matches the handler's regex.

    :param res:
        The requests response object of a stream api
    """
    for msg in res.iter_lines():
        if msg:
            msg = msg.decode('utf-8')
            for handler in handlers:
                if re.match(handler, msg.text):
                    handlers[handler](msg)

def send_message(room_id, msg):
    """
    Send a message to a room

    :param room_id:
        ID of the room to send message to.
    :param msg:
        The message to be sent.
    :returns:
        The response object of the request.
    """

    return requests.post("https://api.gitter.im/v1/rooms/{room_id}/chatMessagges".format(room_id),
                  params={"text": msg})
