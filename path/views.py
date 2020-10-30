import os
import sys
import json
from pathlib import Path

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import ZPath

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
    context['Message'] = 'Hello Moto'

    return render(request, 'path/sandbox.html', context)


def parse_source_query(request):
    
    context = {}

    if request.method == 'POST':
    
        query = request.POST.get('query')


        ytb_obj = ytb.ZYouTube(settings.GGL_KEY)
        resp_dct = ytb_obj.search(query)

        print(json.dumps( resp_dct, indent=4 ))

    #     # Update or create favorite product into db
    #     user_mdl = get_user_model().objects.get(username=request.user.username)
    #     print(request.user)
    #     print(user_mdl)
    #     try:
    #         favorite_mdl = ZProduct.objects.get(code=int(code))
    #     except ZProduct.DoesNotExist:
    #         print("CRITICAL ERROR GETINNG FAVORITE PRODUCT")
    #     else:
    #         if favorite:
    #             user_mdl.favorites.add(favorite_mdl)
    #         else:
    #             user_mdl.favorites.remove(favorite_mdl)
    #         favorite = not favorite
    #         print(favorite)

    #     print(user_mdl.favorites.all())
        context = {'resp' : resp_dct}

    return HttpResponse( json.dumps( context ) )
