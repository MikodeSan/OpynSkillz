from django.urls import path

from . import views

app_name = 'path'

urlpatterns = [
    path('', views.index, name='home'),

    path('lab/', views.lab_view, name='lab'),

    path('lab/path/<int:root_id>', views.path_view, name='path'),

    path('lab/path/new', views.path_create_view, name='new'),
    path('lab/path/root/<int:root_id>/node/<int:node_id>/new', views.path_create_view, name='new'),
    path('lab/path/root/<int:root_id>/node/<int:node_id>/create', views.path_create, name='create'),
    path('lab/path/remove', views.path_remove, name='remove'),
    path('lab/path/move', views.path_move, name='move'),

    path('lab/post/root/<int:root_id>/node/<int:node_id>/new', views.post_initialize, name='post_new'),
    path('lab/post/root/<int:root_id>/node/<int:node_id>/create', views.post_create, name='post_create'),

    # path('lab/sandbox', views.sandbox, name='sandbox'),
    path('lab/path/<int:path_id>/sandbox', views.sandbox, name='sandbox'),
    path('lab/path/<int:path_id>/sandbox/source/<str:source_id>/contents', views.sandbox_source_contents, name='sandbox_source_contents'),
    path('lab/path/sandbox/source/content/add', views.sandbox_content_add, name='content_add'),

    # path('lab/source_query', views.parse_source_query, name='source_query'),      deprecated

    path('lab/parse/subscription', views.add_youtube_channel_2_path, name='channel_subscription'),
]