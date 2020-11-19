import os
import sys
import json
from pathlib import Path
from datetime import datetime

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from . import models



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

PROJECT_DIR = os.path.join(BASE_DIR, 'web_project')
LIB_DIR = os.path.join(BASE_DIR, 'zlibs')

print(BASE_DIR, PROJECT_DIR, LIB_DIR)
sys.path.append(BASE_DIR)
sys.path.append(LIB_DIR)

from zlibs.zapi.google.youtube import youtube as ytb



def index(request):

    # if request.user.is_authenticated:
    context = {}
    context['Message'] = 'Hello Moto'

    # return HttpResponse("Hello, world. You're at the polls index.")

    return render(request, 'path/index.html', context)        # locals()


def lab_view(request):
    
    root_dbo_lst = models.ZTreeNode.objects.root_nodes()

    return render(request, 'path/lab.html', locals())


def path_view(request, root_id):

    root_dbo = models.ZTreeNode.objects.get(pk=root_id)
    node_dbo_lst = root_dbo.get_descendants(include_self=False)

    return render(request, 'path/lab/path.html', locals())


def path_create_view(request, root_id=0, node_id=0):

    element_type = 'path'
        
    return render(request, 'path/path_form.html', locals())


def path_create(request, root_id, node_id):

    ret = redirect('path:lab')

    if request.method == 'POST':
    
        # Create new path
        label = request.POST.get('path_label')
        description = request.POST.get('description')

        path_dbo = models.ZPath.objects.create(label=label, description=description)
        node_dbo = models.ZTreeNode.objects.create(content_object=path_dbo)
        print(node_dbo, node_dbo.content_type, node_dbo.content_object, path_dbo)

        if root_id > 0:

            # Add new path as sub-path
            parent_dbo = models.ZTreeNode.objects.get(pk=node_id)
            node_dbo.move_to(parent_dbo, position='last-child')

            # # Alternative 1
            # parent_dbo.children.add(path_dbo)
            
            # # Alternative 2
            # node_dbo.parent = parent_path_dbo
            # node_dbo.save()
            # node_dbo.refresh_from_db()

            ret = redirect('path:path', root_id)

    return ret


def path_remove(request):

    context = {}

    if request.method == 'POST':
        
        node_id = int(request.POST.get('node_id'))

        models.ZPath.objects.get(pk=node_id).delete()

        context['node_id'] = node_id

    return HttpResponse( json.dumps( context ) )


def path_move(request):
    
    context = {}

    if request.method == 'POST':
        
        operation_id = request.POST.get('operation_id')
        node_id = int(request.POST.get('node_id'))

        path_dbo = models.ZPath.objects.get(pk=node_id)
        
        dbo_lst = models.ZPost.objects.filter(pk=node_id)
        if dbo_lst:
            print('Is Post:', dbo_lst, isinstance(dbo_lst[0], models.ZPost))
        else:
            dbo_lst = models.ZPath.objects.filter(pk=node_id)
            if dbo_lst:
                print('Is Path:', dbo_lst, isinstance(dbo_lst[0], models.ZPath))

        if operation_id == 'parent':
            # Become previous sibling of the parent
            if path_dbo.parent.is_child_node():
                path_dbo.move_to(path_dbo.parent, position='left')

        elif operation_id == 'child':
            # Become first child of the next sibling
            next_path_dbo = path_dbo.get_next_sibling()
            print(path_dbo, next_path_dbo)
            if next_path_dbo:
                path_dbo.move_to(next_path_dbo, position='first-child')

        elif operation_id == 'previous':
            # Become before the previous sibling

            previous_path_dbo = path_dbo.get_previous_sibling()
            if previous_path_dbo:
                path_dbo.move_to(previous_path_dbo, position='left')

        elif operation_id == 'next':
            # Become after the next sibling
            next_path_dbo = path_dbo.get_next_sibling()
            if next_path_dbo:
                path_dbo.move_to(next_path_dbo, position='right')


        if path_dbo.parent:
            parent_id = path_dbo.parent.pk
        else:
            parent_id = 0

        previous_dbo = path_dbo.get_previous_sibling()
        if previous_dbo:
            previous_id = previous_dbo.pk
        else:
            previous_id = 0

        next_dbo = path_dbo.get_next_sibling()
        if next_dbo:
            next_id = next_dbo.pk
        else:
            next_id = 0

        print('PARENT ID', parent_id)
        print('PREVIOUS ID', previous_id)
        print('NEXT ID', next_id)
        print('NODE ID', node_id)

        context['operation_id'] = operation_id
        context['parent_id'] = parent_id
        # context['previous_id'] = previous_id
        context['next_id'] = next_id
        context['node_id'] = node_id

    return HttpResponse( json.dumps( context ) )


def post_initialize(request, root_id=0, node_id=0):

    context = {}

    element_type = 'post'

    return render(request, 'path/path_form.html', locals())

def post_create(request, root_id, node_id):

    ret = redirect('path:path', root_id)

    if request.method == 'POST':
    
        # Create new post
        label = request.POST.get('path_label')
        description = request.POST.get('description')

        post_dbo = models.ZPost.objects.create(label=label, description=description)
        txt_dbo = TextNode.objects.create(extra_text=label)

        if root_id > 0 and node_id > 0:

            # Add new path as sub-path
            path_node_dbo = models.ZPath.objects.get(pk=node_id)
            post_dbo.move_to(path_node_dbo, position='last-child')

            # Add new path as sub-path
            prev_txt_dbo = models.ZPath.objects.get(pk=node_id)
            post_dbo.move_to(path_node_dbo, position='last-child')


            prev_txt_dbo = txt_dbo.get_previous_sibling()
            print(txt_dbo, prev_txt_dbo)
            if prev_txt_dbo:
                txt_dbo.move_to(prev_txt_dbo, position='first-child')


            ret = redirect('path:path', root_id)
        else:
            ret = redirect('path:lab')

    return ret


def sandbox(request, path_id):

    context = {}
    context['path_id'] = path_id
    context['query'] = ''

    if request.method == 'GET':
        
        # get all sources from db
        path_dbo = models.ZPath.objects.get(pk=path_id)
        source_dbo_lst = path_dbo.sources.all()

        if 'query' in request.GET:
            query = request.GET['query']

            if query:

                # search 
                ## get all sources from cloud (Etag to use ?)
                context['query'] = query

                ytb_obj = ytb.ZYouTube(settings.GGL_KEY)
                search_dct = ytb_obj.search(query, is_playlist=False, is_video=False)

                ## Select stored source into db
                channel_lst = search_dct['channel_lst']
                channel_id_lst = [channel_dct['id'] for channel_dct in channel_lst]
                source_dbo_lst = source_dbo_lst.filter(identifier__in=channel_id_lst)

                ## get specific data for each content from cloud (use Etag !) [TODO]

                # Keep only new source from cloud / remove/discard duplicated source from cloud
                for source_dbo in source_dbo_lst:

                    channel_idx = next((idx for idx, channel_dct in enumerate(channel_lst) if source_dbo.identifier == channel_dct['id']), None)

                    ## Update data from cloud data
                    # if source_dbo.etag != channel_lst[channel_idx].etag:
                    # models.ZSource.objects.filter(pk=source_dbo.pk).update()

                    channel_lst.pop(channel_idx)

                # [convert to list to lost of dict or list of db]
                # concatanate list
                
                # send data list



                print(json.dumps( search_dct, indent=4 ))
                context['search_dct'] = search_dct

        context['source_dbo_lst'] = source_dbo_lst 

    return render(request, 'path/sandbox/sandbox.html', context)


def parse_source_query(request):
    
    context = {}

    if request.method == 'POST':
    
        query = request.POST.get('query')


        ytb_obj = ytb.ZYouTube(settings.GGL_KEY)
        resp_dct = ytb_obj.search(query)

        print(json.dumps( resp_dct, indent=4 ))
        context = {'resp' : resp_dct}

    return HttpResponse( json.dumps( context ) )


def add_youtube_channel_2_path(request):

    context = {}

    ipath_id = int(request.POST.get('path_id'))
    sytb_channel_id = request.POST.get('channel_id')
    enable = request.POST.get('enable')

    try:
        path_dbo = models.ZPath.objects.get(pk=ipath_id)
    except ObjectDoesNotExist:
        print("CRITICAL ERROR: ZPath doesn't exist.")
    except MultipleObjectsReturned:
        print("CRITICAL ERROR: ZPath multiple instances")
    else:
        if enable == 'true':

            # update source of contents from cloud
            source_dbo, created = models.ZSource.objects.get_or_create(identifier=sytb_channel_id)

            ytb_obj = ytb.ZYouTube(settings.GGL_KEY)
            etag, channel_dct = ytb_obj.get_channel(source_dbo.identifier)

            param_dct = {}
            param_dct['etag'] = channel_dct['etag']

            snippet_dct = channel_dct['snippet']
            param_dct['label'] = snippet_dct['title']
            # param_dct['url'] = snippet_dct['']
            param_dct['description'] = snippet_dct['description']
            param_dct['published_t'] = datetime.fromisoformat(snippet_dct['publishedAt'].replace('Z', '+00:00')).astimezone(None)  # tz = "Asia/Kolkata" datetime.strptime(snippet_dct['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
            param_dct['thumbnail_url'] = snippet_dct['thumbnails']['high']['url']
            param_dct['country'] = snippet_dct['country']

            stat_dct = channel_dct['statistics']
            param_dct['n_view'] = stat_dct['viewCount']
            param_dct['n_subscriber'] = stat_dct['subscriberCount']
            param_dct['n_content'] = stat_dct['videoCount']
            if 'madeForKids' in channel_dct['status']:
                param_dct['is_4_kid'] = channel_dct['status']['madeForKids']
            
            ZSource.objects.filter(pk=source_dbo.pk).update(**param_dct)

            # if created:
                # get all video from youtube channel

        #                 "customUrl": "marketingmania",
        #                 "": "2015-12-18T10:04:41Z",
        #             },
        #             "contentDetails": {
        #                 "relatedPlaylists": {
        #                     "likes": "",
        #                     "favorites": "",
        #                     "uploads": "UUSmUdD2Dd_v5uqBuRwtEZug",
        #                     "watchHistory": "HL",
        #                     "watchLater": "WL"
        #                 }
        #             },
        #             "status": {
        #                 "madeForKids": false
        #             },
        #             "brandingSettings": {
        #                 "channel": {
        #                     "title": "Marketing Mania",
        #                     "description": "Comment vendre plus efficacement gr\u00e2ce \u00e0 la psychologie humaine.\n\nVid\u00e9os pr\u00e9sent\u00e9es par Stanislas Leloup (Stan Leloup).\n\nPour me contacter, passez par la page contact de mon site web. (marketingmania.fr/contact)",
        #                     "keywords": "marketing \"marketing mania\" \"stan leloup\" \"stanislas leloup\" \"techniques de persuasion\" webmarketing \"technique de vente\" \"optimisation des conversions\" copywriting \"page de vente\" \"vid\u00e9o de vente\"",
        #                     "defaultTab": "Featured",
        #                     "trackingAnalyticsAccountId": "UA-53484520-1",
        #                     "showRelatedChannels": true,
        #                     "showBrowseView": true,
        #                     "featuredChannelsTitle": "Mon autre cha\u00eene :",
        #                     "featuredChannelsUrls": [
        #                         "UCbJP-pDhf7r0tajqXD8Zvpg"
        #                     ],
        #                     "unsubscribedTrailer": "6cJyEEzqMzo",
        #                     "profileColor": "#000000",
        #                     "country": "FR"
        #                 },
        #         }
        #     ]
        # }

            path_dbo.sources.add(source_dbo)
        else:
            source_dbo = models.ZSource.objects.get(identifier=sytb_channel_id)
            path_dbo.sources.remove(source_dbo)

        context['path_id'] = ipath_id
        context['ytb_channel_id'] = sytb_channel_id



    return HttpResponse( json.dumps( context ) )



def sandbox_source_contents(request, path_id, source_id):
    
    context = {}
    context['path_id'] = path_id
    context['source_id'] = source_id

    if request.method == 'GET':
        
        # get source from db
        path_dbo = models.ZPath.objects.get(pk=path_id)
        source_dbo = path_dbo.sources.filter(identifier=source_id).get()

        # get source contents from db
        content_dbo_lst = source_dbo.contents.all()
        print(content_dbo_lst)

        # Update
        if True: # len(content_dbo_lst) < source_dbo.n_content:

            ytb_obj = ytb.ZYouTube(settings.GGL_KEY)
            content_dct_lst = ytb_obj.get_video_from_channel(channel_id=source_id)

            # update or create content
            for content_dct in content_dct_lst:

                # get content from db based on id
                content_dbo, created = models.ZContent.objects.get_or_create(identifier=content_dct['id'])

                # update
                content_dct = {
                    'label': content_dct['title'],
                    'description': content_dct['description'],
                    'thumbnail_url': content_dct['thumbnail_url'],
                    'published_t': datetime.fromisoformat(content_dct['published_t'].replace('Z', '+00:00')).astimezone(None),  # tz = "Asia/Kolkata"
                }
                models.ZContent.objects.filter(pk=content_dbo.pk).update(**content_dct)
                # content_dbo = models.ZContent.objects.get(pk=content_dbo.pk)
                source_dbo.contents.add(content_dbo)
                print(content_dbo, 'Created:', created)


            # get source contents from db
            content_dbo_lst = source_dbo.contents.all()
            print(content_dbo_lst)


        # if 'query' in request.GET:
        #     query = request.GET['query']

        #     if query:

        #         # search 
        #         ## get all sources from cloud (Etag to use ?)
        #         context['query'] = query


        #         ## Select stored source into db
        #         channel_lst = search_dct['channel_lst']
        #         channel_id_lst = [channel_dct['id'] for channel_dct in channel_lst]
        #         source_dbo_lst = source_dbo_lst.filter(identifier__in=channel_id_lst)

        #         ## get specific data for each content from cloud (use Etag !) [TODO]

        #         # Keep only new source from cloud / remove/discard duplicated source from cloud
        #         for source_dbo in source_dbo_lst:

        #             channel_idx = next((idx for idx, channel_dct in enumerate(channel_lst) if source_dbo.identifier == channel_dct['id']), None)

        #             ## Update data from cloud data
        #             # if source_dbo.etag != channel_lst[channel_idx].etag:
        #             # models.ZSource.objects.filter(pk=source_dbo.pk).update()

        #             channel_lst.pop(channel_idx)

        #         # [convert to list to lost of dict or list of db]
        #         # concatanate list
                
        #         # send data list

        #         print(json.dumps( search_dct, indent=4 ))
        #         context['search_dct'] = search_dct

            context['content_dbo_lst'] = content_dbo_lst.order_by('-published_t')

        context['path_dbo_lst'] = path_dbo.get_descendants(include_self=False)

    return render(request, 'path/sandbox/content.html', context)


def sandbox_content_add(request):

    context = {}

    iroot_path_id = int(request.POST.get('root_path_id'))
    ipath_id = int(request.POST.get('path_id'))
    sytb_channel_id = request.POST.get('channel_id')
    icontent_id = int(request.POST.get('content_id'))
    enable = request.POST.get('enable')

    
    content_dbo = models.ZContent.objects.get(pk=icontent_id)

    if ipath_id:
        path_dbo = models.ZPath.objects.get(pk=ipath_id)
    else:
        path_dbo = models.ZPath.objects.get(pk=iroot_path_id).get_children()[0]

    print('Store: Content {} to Path {}'.format(content_dbo, path_dbo))

    return HttpResponse( json.dumps( context ) )


