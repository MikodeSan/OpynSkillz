from django.urls import path

from . import views

app_name = 'path'

urlpatterns = [
    path('', views.index, name='home'),
    path('channel/', views.channel, name='channel'),
    path('channel/path/new', views.path_new, name='path_new'),
    path('channel/path/create', views.create_path, name='path_create'),
    path('channel/sandbox', views.sandbox, name='sandbox'),
    path('channel/<int:path_id>/sandbox', views.sandbox, name='sandbox'),
    # path('channel/source_query', views.parse_source_query, name='source_query'),      deprecated

    path('channel/parse/subscription', views.add_youtube_channel_2_path, name='channel_subscription'),
      
]