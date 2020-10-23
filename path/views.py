from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import ZPath



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

    print('Path label:', request)

    if request.method == 'POST':
    
        label = request.POST.get('path_label')
        description = request.POST.get('description')
        print('Path label: {}, Description: {}'.format(label, description))

        path_dbo = ZPath.objects.create(label=label, description=description)

    return redirect('path:channel')


