import uuid , random
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
             player = Player.objects.create(name=name, room=room)
             request.session["player_id"] = player.id
             return redirect("room", code=room.code)


        

        # Join Room
        if "join" in request.POST:
            try:
                room = Room.objects.get(code=code)
            except Room.DoesNotExist:
                return render(request, "game/home.html", {"error": "Room not found"})

            player = Player.objects.create(name=name, room=room)
            request.session["player_id"] = player.id
            return redirect("room", code=room.code)

    return render(request, "game/home.html")

def room(request, code):
    room = Room.objects.get(code=code)
    players = room.players.all()

    player_id = request.session.get("player_id")
    current_player = None

    if player_id:
        current_player = Player.objects.filter(id=player_id).first()

    return render(request, "game/room.html", {
        "room": room,
        "players": players,
        "current_player": current_player,
    })


def generate_room_code():
    return str(uuid.uuid4())[:6].upper()

def start_game(request, code):
    room = Room.objects.get(code = code)
    players = list(room.players.all())

    if len(players) < 3:
        return redirect("room", code = room.code)
    
    random.shuffle(players)

    players[0].role = "chor"
    players[0].save()

    players[1].role ="police"
    players[1].save()


    for player in players[2:]:
        player.role = 'citizen'
        player.save()


    gamestate= GameState.objects.get(room=room)   
    gamestate.phase = "reveal" 
    gamestate.save()

    return redirect("room", code=room.code)




























