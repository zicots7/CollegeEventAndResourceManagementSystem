from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Events
from registration.models import Registration
from .form import EventForm
from . import eventRequest
from user.decorators import (
role_required
)
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
    if request.method == "POST":
        form = EventForm(request.POST,instance=event)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f" Event  -- {event.title} -- is successfully Updated"
            )
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
        messages.warning(
            request,
            f" Event  -- {event.title} -- is successfully Deleted"
        )
        return redirect('event_lists')
    return render(request,'DeleteEvent.html',{'event':event})


@role_required(allowed_roles=['Admin','Faculty','Student'])
def event_lists(request):
    events = Events.objects.all()
    return render(request,'EventList.html',{'events':events})

@role_required(allowed_roles=['Admin'])
def event_notification(request,id):
    event = Events.objects.get(id=id)
    if request.method == 'POST':
        if event.reminder_sent:
            event.reminder_sent = False
        else:
            event.reminder_sent = True
        event.save()
        return redirect('event_lists')
    return render(request,'PushNotification.html',{'events':event})