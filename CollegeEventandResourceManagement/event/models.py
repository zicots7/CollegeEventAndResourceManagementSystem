from django.db import models
from django.conf import settings
from django.utils import timezone


class Events(models.Model):
    status_choices= [("Complete","Complete"),
              ("Upcoming","Upcoming"),
              ("Ongoing","Ongoing"),
              ("Cancelled","Cancelled"),
              ]
    status = models.CharField(choices=status_choices,null=False)
    type_choices = [
        ('Seminar', 'Seminar'),
        ('Workshop', 'Workshop'),
        ('Placement', 'Placement Drive'),
        ('Cultural', 'Cultural'),
        ('Sports', 'Sports'),
        ('Other', 'Other'),
    ]
    type = models.CharField(choices=type_choices,null=False)
    title = models.CharField(null=False,max_length=200)
    description = models.TextField(null=False)
    date = models.DateTimeField()
    venue = models.CharField(max_length=200)
    capacity = models.IntegerField()
    department = models.CharField(
        max_length=100,
        blank=False,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_events'
    )
    created_at = models.DateTimeField(default=timezone.now)
    reminder_sent = models.BooleanField(default=False)
    class Meta:
        db_table = "events"
        ordering = ['date']
    def __str__(self):
        return self.title
    def is_full(self):
        return self.registrations.count() >= self.capacity
    def spots_remaining(self):
        return self.capacity - self.registrations.count()

