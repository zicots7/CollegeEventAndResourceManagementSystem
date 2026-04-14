from django.db import models
from django.conf import settings
class Registration(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='registrations'
    )
    event = models.ForeignKey(
        'event.Events',
        on_delete=models.CASCADE,
        related_name='registrations'
    )
    registered_at = models.DateTimeField(auto_now_add=True)
    attended = models.BooleanField(default=False)
    class Meta:
        db_table = 'registration'
        unique_together = ['student', 'event']

    def __str__(self):
        return f"{self.student.username} - {self.event.title}"

