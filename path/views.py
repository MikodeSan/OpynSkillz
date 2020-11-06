import os
import sys
import json
from pathlib import Path
from datetime import datetime

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from .models import ZPath, ZContentSource

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


def channel(request):
    
    context = {}
    context['Message'] = 'Hello Moto'

    # path_lst_dbo = ZPath.objects.all()
    context['path_dbo_lst'] = ZPath.objects.all()

    return render(request, 'path/channel.html', context)


def path_new(request):

    context = {}
    context['Message'] = 'Hello Moto'

    return render(request, 'path/path_new.html', context)


def create_path(request):

    context = {}
    context['Message'] = 'Hello Moto'

    if request.method == 'POST':
    
        label = request.POST.get('path_label')
        description = request.POST.get('description')
        
        path_dbo = ZPath.objects.create(label=label, description=description)

    return redirect('path:channel')


def sandbox(request, path_id):

    context = {}
    context['path_id'] = path_id
    context['query'] = ''

    if request.method == 'GET':
        
        # get all sources from db
        path_dbo = ZPath.objects.get(pk=path_id)
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
                    # ZContentSource.objects.filter(pk=source_dbo.pk).update()

                    channel_lst.pop(channel_idx)

                # [convert to list to lost of dict or list of db]
                # concatanate list
                
                # send data list



                print(json.dumps( search_dct, indent=4 ))
                context['search_dct'] = search_dct

        context['source_dbo_lst'] = source_dbo_lst 

    return render(request, 'path/sandbox.html', context)


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
        path_dbo = ZPath.objects.get(pk=ipath_id)
    except ObjectDoesNotExist:
        print("CRITICAL ERROR: ZPath doesn't exist.")
    except MultipleObjectsReturned:
        print("CRITICAL ERROR: ZPath multiple instances")
    else:
        if enable == 'true':

            # update source of contents from cloud
            source_dbo, created = ZContentSource.objects.get_or_create(identifier=sytb_channel_id)

            ytb_obj = ytb.ZYouTube(settings.GGL_KEY)
            etag, channel_dct = ytb_obj.get_channel(source_dbo.identifier)

            param_dct = {}
            param_dct['etag'] = channel_dct['etag']

            snippet_dct = channel_dct['snippet']
            param_dct['label'] = snippet_dct['title']
            # param_dct['url'] = snippet_dct['']
            param_dct['description'] = snippet_dct['description']
            param_dct['published_t'] = datetime.strptime(snippet_dct['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')             
            param_dct['thumbnail_url'] = snippet_dct['thumbnails']['high']['url']
            param_dct['country'] = snippet_dct['country']

            stat_dct = channel_dct['statistics']
            param_dct['n_view'] = stat_dct['viewCount']
            param_dct['n_subscriber'] = stat_dct['subscriberCount']
            param_dct['n_content'] = stat_dct['videoCount']
            if 'madeForKids' in channel_dct['status']:
                param_dct['is_4_kid'] = channel_dct['status']['madeForKids']
            
            ZContentSource.objects.filter(pk=source_dbo.pk).update(**param_dct)

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
            source_dbo = ZContentSource.objects.get(identifier=sytb_channel_id)
            path_dbo.sources.remove(source_dbo)

        context['path_id'] = ipath_id
        context['ytb_channel_id'] = sytb_channel_id



    return HttpResponse( json.dumps( context ) )
