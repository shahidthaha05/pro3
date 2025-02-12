from django.db import models

class Game(models.Model):
    g_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    release_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.FileField()
    
    def __str__(self):
        return self.title


class Slot(models.Model):
    game = models.ForeignKey(Game, related_name='slots', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    reserved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.game.title}: {self.start_time} - {self.end_time}"


