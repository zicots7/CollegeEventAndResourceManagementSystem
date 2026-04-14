from django.db import models
from django.conf import settings
from django.utils import timezone

class Resource(models.Model):
    CATEGORY_CHOICES = [
        ('Notes', 'Notes'),
        ('Assignment', 'Assignment'),
        ('Syllabus', 'Syllabus'),
        ('Previous_paper', 'Previous Year Paper'),
        ('Reference', 'Reference Material'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    subject = models.CharField(max_length=100)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='notes'
    )
    Departments =[
                    ('MCA', 'MCA'),
                    ('BCA', 'BCA'),
                    ('BSc CS', 'BSc CS'),
                    ('MSc DS', 'MSc Data Science'),
                ]
    department = models.CharField(choices=Departments,max_length=100)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='uploaded_resources'
    )
    uploaded_at = models.DateTimeField(default=timezone.now)
    download_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'resource'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.title} - {self.subject}"