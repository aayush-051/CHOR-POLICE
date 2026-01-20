from django.db import models
import uuid

# Create your models here.

class Room(models.Model):
    code = models.CharField(max_length=6, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code
    
class Player(models.Model):
    ROLES_CHOICES = [
        ('chor','Chor'),
        ('police','Police'),
        ('citizen','Citizen'),

    ]


    room = models.ForeignKey(Room , on_delete=models.CASCADE ,related_name="players")
    name = models.CharField(max_length=50)
    role = models.CharField(max_length=10, choices=ROLES_CHOICES , blank=True)
    is_alive = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.room.code}) "
    
class GameState(models.Model):
    PHASE_CHOICES = [
        ('lobby', 'Lobby'),
        ('reveal', 'Role Reveal'),
        ('discussion', 'Discussion'),
        ('police_turn', 'Police Turn'),
        ('result', 'Result'),
    ]
    room = models.OneToOneField(Room, on_delete=models.CASCADE)  
    phase = models.CharField(max_length=20, choices= PHASE_CHOICES, default="lobby")  
    winner = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.room.code} -{self.phase} "



