from django.db import models
from django.utils.timezone import now, timedelta
from datetime import date

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
    TIME_SLOT_CHOICES = [
        ('10:00 AM - 12:00 PM', '10:00 AM - 12:00 PM'),
        ('12:00 PM - 2:00 PM', '12:00 PM - 2:00 PM'),
        ('2:00 PM - 4:00 PM', '2:00 PM - 4:00 PM'),
        ('4:00 PM - 6:00 PM', '4:00 PM - 6:00 PM'),
        ('6:00 PM - 8:00 PM', '6:00 PM - 8:00 PM'),
    ]

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="slots")
    date = models.DateField()
    time_slot = models.CharField(max_length=20, choices=TIME_SLOT_CHOICES)
    reserved = models.BooleanField(default=False)
    booking_time = models.DateTimeField(null=True, blank=True)  # Track when booked

    def is_expired(self):
        """Check if booking has expired (after 24 hours)."""
        if self.reserved and self.booking_time:
            return now() > self.booking_time + timedelta(days=1)
        return False

    def save(self, *args, **kwargs):
        """Automatically reset slot status if expired."""
        if self.is_expired():
            self.reserved = False
            self.booking_time = None
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('game', 'date', 'time_slot')

    def __str__(self):
        status = "Booked" if self.reserved else "Available"
        return f"{self.game.title} - {self.date} - {self.time_slot} ({status})"


from django.db import models
from django.utils.timezone import now

class SlotBooking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    date = models.DateField()
    booking_time = models.DateTimeField(default=now)  # Manually set the default value here

    def __str__(self):
        return f"{self.name} - {self.game.title} on {self.date} at {self.slot.time_slot}"

