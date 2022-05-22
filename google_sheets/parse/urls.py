from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index),
    path('start', views.start_scripts),
    path('stop', views.stop_scripts)
]

