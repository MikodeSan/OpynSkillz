from django.urls import path

from . import views

app_name = 'path'

urlpatterns = [
    path('', views.index, name='home'),
    path('channel/', views.channel, name='channel'),
    path('channel/path/new', views.path_initialize, name='new'),
    path('channel/path/new/root/<int:root_id>/parent/<int:parent_id>', views.path_initialize, name='new'),
    path('channel/path/create/root/<int:root_id>/parent/<int:parent_id>', views.path_create, name='create'),
    path('channel/design/path/<int:path_id>', views.path_design, name='design'),
    # path('channel/sandbox', views.sandbox, name='sandbox'),
    path('channel/design/path/<int:path_id>/sandbox', views.sandbox, name='sandbox'),
    path('channel/design/path/<int:path_id>/sandbox/source/<str:source_id>/contents', views.sandbox_source_contents, name='sandbox_source_contents'),
    # path('channel/source_query', views.parse_source_query, name='source_query'),      deprecated

    path('channel/parse/subscription', views.add_youtube_channel_2_path, name='channel_subscription'),
      
]