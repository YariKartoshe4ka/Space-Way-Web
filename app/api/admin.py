from django.contrib import admin

from .models import versions, get_replay_model


for version in versions:
    admin.site.register(get_replay_model(version))
