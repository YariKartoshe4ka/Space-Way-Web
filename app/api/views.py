from re import match

from django.views.decorators.csrf import csrf_exempt

from .models import Replay
from .utils import api_request


@csrf_exempt
@api_request(methods=['POST'], schema='start')
def start(request, body):
    """Starts replay submission

    Args:
        nick (str): Player nick

    Returns:
        id (str): The replay ID. You need it to upload the replay itself later
        state (str): Initial state of the randomizer
    """
    # Validate body
    if not match(r'^[\w!?$%]{1,15}$', body['nick']):
        return {
            'status': 400,
            'description': 'Nick has an invalid format'
        }

    # Perform request
    replay = Replay(nick=body['nick'], ip=request.META['REMOTE_ADDR'])
    replay.save()

    return {
        'status': 200,
        'result': {
            'id': replay.id,
            'state': replay.state
        }
    }
