import uuid
from .models import Player,Room,GameState
from django.shortcuts import render, redirect
from django.http import HttpResponse   #this line is safe to remove since HttpResponse is not used

# Create your views here.

def home(request):
    if request.method == "POST":
        name = request.POST.get("name")
        code = request.POST.get("code")

        if not name:
            return render(request, "game/home.html", {"error": "Name is required"})    
        
        #Create Room
        
        if "create" in request.POST:
             room = Room.objects.create(code=generate_room_code())
             GameState.objects.create(room=room)
             Player.objects.create(name=name, room=room)
             return redirect("room", code=room.code)


        

        # Join Room
        if "join" in request.POST:
            try:
                room = Room.objects.get(code=code)
            except Room.DoesNotExist:
                return render(request, "game/home.html", {"error": "Room not found"})

            Player.objects.create(name=name, room=room)
            return redirect("room", code=room.code)

    return render(request, "game/home.html")

def room(request, code):
    room = Room.objects.get(code=code)
    players = room.players.all()

    return render(request, "game/room.html", {
        "room": room,
        "players": players
    })


def generate_room_code():
    return str(uuid.uuid4())[:6].upper()

























