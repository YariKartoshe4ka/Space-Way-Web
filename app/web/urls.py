from django.urls import path

from . import views


urlpatterns = [
    path('', views.index),
    path('<str:version>', views.index)
]
