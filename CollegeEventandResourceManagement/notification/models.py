from django.db import models
from event.models import Events
from django.conf import settings

class Notifications(models.Model):
    notification_id=models.CharField(max_length=400)
    event = models.ForeignKey(Events, on_delete=models.CASCADE,related_name='notifications')
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    class Meta:
        db_table = "notifications"