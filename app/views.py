from django.shortcuts import render

# Create your views here.
from django.shortcuts import render


def index(request):
    return render(request, "app/index.html")


"""def room(request, room_name):
    return render(request, "app/room.html", {"room_name": room_name})
"""


def trans(request):
    return render(request, "app/translate.html")


