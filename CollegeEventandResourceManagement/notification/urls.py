from django.urls import path
from .views import(
event_notification
)
urlpatterns = [
    path('event_notification/<int:id>',event_notification,name='event_notification'),
]