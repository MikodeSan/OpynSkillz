from django.http import HttpResponse
from django.shortcuts import render



def index(request):

    # if request.user.is_authenticated:

    context = {}
    context['Message'] = 'Hello Moto'

    # return HttpResponse("Hello, world. You're at the polls index.")

    return render(request, 'path/index.html', context)        # locals()





