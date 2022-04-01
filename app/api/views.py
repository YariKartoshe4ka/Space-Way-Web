from re import match

from .models import Replay
from .utils import api_method


@api_method(methods=['GET'])
def get(request, body):
    """Gets information about the top 5 replays

    Returns:
        score (int): The final score in this replay
        nick (str): Nickname of the player who created the replay
    """

    response = {'status': 200, 'result': []}

    replays = Replay.objects \
        .filter(status='approved') \
        .order_by('-score', 'date_end')

    for replay in replays[:5].values_list('score', 'nick'):
        response['result'].append(replay)

    return response


@api_method(methods=['POST'], schema='start')
def start(request, body):
    """Starts replay submission

    Args:
        nick (str): Player nick

    Returns:
        id (str): The replay ID. You need it to upload the replay itself later
        state (str): Initial state of the randomizer
    """

    # Validate body
    if not match(r'^[\w!?:; \(\)]{1,15}$', body['nick']):
        return {
            'status': 400,
            'description': 'Nick has an invalid format'
        }

    # Perform request
    replay = Replay(nick=body['nick'])
    replay.save()

    return {
        'status': 200,
        'result': {
            'id': replay.id,
            'state': replay.state
        }
    }
