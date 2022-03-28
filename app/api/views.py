from json import loads, load
from re import match
import os

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseNotAllowed
from jsonschema import validate

from .models import Replay
from .utils import api_response


CUR_DIR = os.path.dirname(__file__)


with open(CUR_DIR + '/schemas/start.json') as file:
    schema_start = load(file)


@csrf_exempt
@api_response
def start(request):
    """Starts replay submission

    Method: POST

    Args:
        nick (str): Player nick

    Returns:
        id (str): The replay ID. You need it to upload the replay itself later
        state (str): Initial state of the randomizer
    """
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    # Validate body
    body = request.body.decode()

    try:
        body = loads(body)
        validate(instance=body, schema=schema_start)

    except Exception:
        return {
            'status': 400,
            'description': 'Body has an invalid JSON object'
        }

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
