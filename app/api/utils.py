from base64 import b64encode
from json import load, loads
from multiprocessing import Process, Queue
from pickle import dumps
from random import getstate
import os

from django.http import JsonResponse
from jsonschema import validate


CUR_DIR = os.path.dirname(__file__)


def random_getstate():
    """Generates state of `random.getstate`. To ensure the uniqueness of the
    resulting value, the function is executed in a separate process (with
    separate memory) via multiprocessing

    Returns:
        str: `getstate` value, previously dumped via `pickle` and encoded
            in base64
    """
    # Set queue to communicate with process
    q = Queue()

    # Define process and start it
    p = Process(target=lambda q: q.put(getstate()), args=(q,))
    p.start()
    p.join()

    # Return value, dumped via `pickle` and encoded in base64
    return b64encode(dumps(q.get())).decode()


# Load all API schemas
api_schemas = {}

for name in os.listdir(f'{CUR_DIR}/schemas'):
    # Get absolute path to JSON in `schemas` directory
    path = os.path.join(CUR_DIR, 'schemas', name)

    if os.path.isfile(path) and path.endswith('.json'):
        with open(path) as file:
            api_schemas[name[:-5]] = load(file)


def api_request(methods, schema):
    """Decorator for API requests and them responses

    Args:
        schema (str): Name of file (without ".json" extension) with JSON schema
            of current request arguments

    The API response has the following structure:

    .. code-block:: json

        {
            "status": number,        // Has the same meaning as HTTP response code
            "description": string    // Description of the fail/success of the request
            "result": null | object  // `null` in case of failure, object in case of success
        }

    Example:

        .. code-block:: python

            @api_request(methods=['POST'], schema='start')
            def api_view(request, body):
                return {
                    'status': 200,
                    'result': 'Thanks!'
                }
    """
    def decorator(func):
        """

        Args:
            func (callable): The function to decorate. Must return at least the
                status in `dict` object
        """
        def wrapper(request, *args, **kwargs):
            if request.method not in methods:
                response = {
                    'status': 405,
                    'description': f"Method not allowed. Permitted methods: {', '.join(methods)}",
                    'result': None
                }

                return JsonResponse(response, safe=True)

            body = request.body.decode()

            try:
                body = loads(body)
                validate(instance=body, schema=api_schemas[schema])

            except Exception:
                response = {
                    'status': 400,
                    'description': 'Body has an invalid JSON object',
                    'result': None
                }

                return JsonResponse(response, safe=True)

            raw_response = func(request, body, *args, **kwargs)

            response = {}
            response['status'] = raw_response['status']
            response['description'] = raw_response.get('description', 'Request successfully processed')
            response['result'] = raw_response.get('result')

            return JsonResponse(response, safe=True)

        return wrapper

    return decorator
