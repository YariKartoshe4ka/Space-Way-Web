from django.shortcuts import render
from django.http import Http404

from api.models import versions


def index(request, version=None):
    if version and version not in versions:
        raise Http404

    context = {
        'cur_version': version or versions[-1],
        'versions': versions
    }

    return render(request, 'index.html', context=context)
