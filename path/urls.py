from django.urls import path

from . import views

app_name = 'path'

urlpatterns = [
    path('', views.index, name='home'),
    path('channel/', views.channel, name='channel'),
    path('channel/path/new', views.path_new, name='path_new'),
    path('channel/path/create', views.create_path, name='path_create'),


    
]