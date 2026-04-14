from django.urls import path
from .views import(
download,
)
urlpatterns = [
    path('download/<int:id>',download,name='download-resource'),
]