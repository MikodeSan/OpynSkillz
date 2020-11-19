from django.urls import path

from . import views

app_name = 'path'

urlpatterns = [
    path('', views.index, name='home'),
    path('channel/', views.channel, name='channel'),

    path('channel/design/path/<int:path_id>', views.path_design, name='design'),

    path('channel/path/new', views.path_initialize, name='new'),
    path('design/path/root/<int:root_id>/node/<int:node_id>/new', views.path_initialize, name='new'),
    path('design/path/root/<int:root_id>/node/<int:node_id>/create', views.path_create, name='create'),
    path('channel/path/remove', views.path_remove, name='remove'),
    path('channel/path/move', views.path_move, name='move'),

    path('design/post/root/<int:root_id>/node/<int:node_id>/new', views.post_initialize, name='post_new'),
    path('design/post/root/<int:root_id>/node/<int:node_id>/create', views.post_create, name='post_create'),

    # path('channel/sandbox', views.sandbox, name='sandbox'),
    path('channel/design/path/<int:path_id>/sandbox', views.sandbox, name='sandbox'),
    path('channel/design/path/<int:path_id>/sandbox/source/<str:source_id>/contents', views.sandbox_source_contents, name='sandbox_source_contents'),
    path('channel/design/path/sandbox/source/content/add', views.sandbox_content_add, name='content_add'),

    # path('channel/source_query', views.parse_source_query, name='source_query'),      deprecated

    path('channel/parse/subscription', views.add_youtube_channel_2_path, name='channel_subscription'),
      
]