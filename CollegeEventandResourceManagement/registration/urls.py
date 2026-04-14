from django.urls import path
from .views import(
    EventRegister,
    RegisteredList,
    AttendedEvent,
    CancelRegistration,
)
urlpatterns = [
    path('register/<int:id>',EventRegister,name='EventRegister'),
    path('RegisteredList/',RegisteredList,name='RegisteredList'),
    path('AttendedEvent/<int:id>',AttendedEvent,name='AttendedEvent'),
    path('CancelRegistration/<int:id>',CancelRegistration,name='CancelRegistration'),
]