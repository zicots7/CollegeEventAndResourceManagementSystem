from django.db import models
from django.conf import settings
from resources.models import Resource
class ResourceDownload(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='downloads'
    )
    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        related_name='download_records'
    )
    downloaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'resource_download'

    def __str__(self):
        return f"{self.student.username} - {self.resource.title}"