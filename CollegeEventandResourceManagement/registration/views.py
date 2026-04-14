from django.shortcuts import render,redirect
from .models import Registration
from event.models import Events
from user.decorators import role_required
from django.contrib import messages
@role_required(allowed_roles=['Admin','Faculty'])
def RegisteredList(request):
    registration = Registration.objects.all()
    return render(request,'RegisteredList.html',{'registration':registration})
@role_required(allowed_roles=['Student'])
def EventRegister(request,id):
    event = Events.objects.get(id=id)
    already_registered = Registration.objects.filter(
        student=request.user,
        event=event
    ).exists()
    if already_registered:
        messages.info(request, "You are already registered for this event.")
        return redirect('event_lists')
    if event.is_full():
        messages.warning(request, "Sorry this event is full.")
        return redirect('event_lists')
    if event.status != 'Upcoming':
        messages.warning(request, "Registration is closed for this event.")
        return redirect('event_lists')
    if request.method == 'POST':
        registered=Registration.objects.create(
            student=request.user,
            event=event
        )
        registered.save()
        messages.success(request,f"Successfully registered for {event.title}")
        return redirect('event_lists')
    context = {'event': event}
    return render(request, 'EventList.html', context)

@role_required(allowed_roles=['Student'])
def CancelRegistration(request,id):
    event = Events.objects.get(id=id)
    registration = Registration.objects.filter(
        student=request.user,
        event=event
    )
    if request.method == 'POST':
        if Registration.objects.filter(student=request.user, event=event).exists():
            registration.delete()
            messages.info(request,f"Registration is cancelled for {event.title}")
        elif not Registration.objects.filter(student=request.user, event=event).exists():
            messages.info(request, f"Registration is already cancelled for --{event.title}-- event. ")
        else:
            messages.info(request, f"You are not registered for this --{event.title}-- event. ")
        return redirect('event_lists')
@role_required(allowed_roles=['Admin','Faculty'])
def AttendedEvent(request,id):
    registered = Registration.objects.get(id=id)
    registered.attended = not registered.attended
    registered.save()
    return redirect('RegisteredList')