
from django.urls import path
from .views import(
addEvent,
updateEvent,
deleteEvent,
event_lists,

)

urlpatterns=[
    path('event_lists/',event_lists,name='event_lists'),
    path('addEvent/',addEvent,name='addEvent'),
    path('updateEvent/<int:id>',updateEvent,name='updateEvent'),
    path('deleteEvent/<int:id>',deleteEvent,name='deleteEvent'),


]