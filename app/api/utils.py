from multiprocessing import Process, Queue
from pickle import dumps
from random import getstate
from base64 import b64encode

from django.http import JsonResponse


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


def api_response(func):
    """Decorator for API responses

    Args:
        func (callable): The function to decorate. Must return at least the
            status in `dict` object

    The API response has the following structure:

    .. code-block:: json

        {
            "status": number,        // Has the same meaning as HTTP response code
            "description": string    // Description of the fail/success of the request
            "result": null | object  // `null` in case of failure, object in case of success
        }
    """
    def wrapper(*args, **kwargs):
        response = {}
        raw_response = func(*args, **kwargs)

        response['status'] = raw_response['status']
        response['description'] = raw_response.get('description', 'Request successfully processed')
        response['result'] = raw_response.get('result')

        return JsonResponse(response, safe=True)

    return wrapper
