from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Events
from notification.models import Notifications
from notification.views import turnOffNotifiation,turnOnNotification
from django.utils import timezone
from django.contrib.auth import(
    get_user_model
)
from .form import EventForm
from user.decorators import (
role_required
)
users= get_user_model()
@role_required(allowed_roles=['Admin','Faculty'])
def addEvent(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event_instance = form.save(commit=False)
            event_instance.created_by = request.user
            form.save()
            messages.success(
                request,
                f" Event  -- {event_instance.title} -- is successfully Added"
            )
            return redirect('event_lists')
    else:
        form = EventForm()
    return render(request,'AddEvent.html',{'form':form})

@role_required(allowed_roles=['Admin','Faculty'])
def updateEvent (request,id):
    event = Events.objects.get(id=id)
    registered = event.registrations.all().select_related('student')
    if request.method == "POST":
        form = EventForm(request.POST,instance=event)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f" Event  -- {event.title} -- is successfully Updated"
            )
            event_notification = Notifications.objects.filter(event_id=event.id)
            for entry in event_notification:
                turnOffNotifiation(entry.notification_id)
            event_notification.delete()
            activated_count = 0
            if registered.exists():
               if event.reminder_sent == True:
                for students in registered:
                    objs = students.student
                    notification_id = turnOnNotification(
                        eventTime=event.date,
                        eventName=event.title,
                        email=objs.email,
                        firstname=objs.first_name,
                        lastname=objs.last_name,
                        department=objs.department,
                        venue=event.venue
                    )
                    if notification_id:
                        Notifications.objects.create(notification_id=notification_id,
                                                     event_id=event.id,
                                                     student=objs
                                                     )
                        activated_count += 1
                messages.success(request, f"Notification Rescheduled Successfully for the event -- {event.title} .")
            return redirect('event_lists')
    else:
        form = EventForm(instance=event)
    return render(request,'EditEvent.html',{'form':form})

@role_required(allowed_roles=['Admin'])
def deleteEvent(request,id):
    event = Events.objects.get(id=id)
    if request.method == "POST":
        event = Events.objects.get(id=id)
        event.delete()
        event_notification = Notifications.objects.filter(event_id=event.id)
        for entry in event_notification:
            turnOffNotifiation(entry.notification_id)
        event_notification.delete()
        messages.warning(
            request,
            f" Event  -- {event.title} -- is successfully Deleted and Event Notification Cancelled."
        )
        return redirect('event_lists')
    return render(request,'DeleteEvent.html',{'event':event})


@role_required(allowed_roles=['Admin','Faculty','Student'])
def event_lists(request):
    current_time = timezone.now()
    events = Events.objects.all()
    for event in events:
        if event.date <= current_time :
            event.status = "Complete"
        event.save()
        events = Events.objects.all()
    return render(request,'EventList.html',{'events':events})

