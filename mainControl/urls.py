
from django.urls import path,include

from mainControl import views
appname = 'mainControl'
urlpatterns = [
    path('index/',views.index),
    path('index_data/',views.index_data),
]