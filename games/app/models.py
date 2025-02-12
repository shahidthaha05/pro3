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


from django.db import models
from django.utils.timezone import now, timedelta

class Slot(models.Model):
    TIME_SLOT_CHOICES = [
        ('10:00 AM - 12:00 PM', '10:00 AM - 12:00 PM'),
        ('12:00 PM - 2:00 PM', '12:00 PM - 2:00 PM'),
        ('2:00 PM - 4:00 PM', '2:00 PM - 4:00 PM'),
        ('4:00 PM - 6:00 PM', '4:00 PM - 6:00 PM'),
        ('6:00 PM - 8:00 PM', '6:00 PM - 8:00 PM'),
    ]

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="slots")
 
    time_slot = models.CharField(max_length=20, choices=TIME_SLOT_CHOICES)
    reserved = models.BooleanField(default=False)
    booking_time = models.DateTimeField(null=True, blank=True)  # Track when slot was booked

    class Meta:
        unique_together = ('game', 'time_slot')

    def is_available(self):
        """Returns True if slot was booked over an hour ago or is unbooked."""
        if not self.reserved:
            return True  # Not booked, so it's available
        if self.booking_time and now() >= self.booking_time + timedelta(hours=1):
            return True  # 1 hour passed, make it available again
        return False  # Still within 1-hour limit

    def __str__(self):
        return f"{self.game.title} - {self.time_slot} ({'Booked' if self.reserved else 'Available'})"


from django.db import models

class SlotBooking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    game = models.CharField(max_length=100)
    date = models.DateField()
    time_slot = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} - {self.game} on {self.date} at {self.time_slot}"
