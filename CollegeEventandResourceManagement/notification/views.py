from django.shortcuts import render,redirect
from django.contrib import messages
from django.utils import timezone
from zoneinfo import ZoneInfo
from user.decorators import role_required
from registration.models import Registration
from event.models import Events
from .models import Notifications
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import requests
from django.http import HttpResponse
load_dotenv()
def turnOnNotification(eventName,eventTime,firstname,lastname,email,department,venue):
    spring_uri=os.getenv("SPRING_URI_SCHEDULE")
    local_dt = eventTime.astimezone(ZoneInfo("Asia/Kolkata"))
    new_dt = local_dt - timedelta(days=1)
    formatted_date = new_dt.strftime('%Y-%m-%dT%H:%M:%S')
    nice_looking_time = local_dt.strftime('%B %d, %Y, %I:%M %p')
    body_data = {
        'to': email,
        'subject': f" A gentle reminder for the event -- {eventName} -- .",
        'body': (f"Hello,\n"
                 f" {firstname} {lastname} \n from {department} department,\n\n\n\n"
                 f"This is a gentle reminder just to let you know you have to attend the event --- {eventName} --- on {nice_looking_time} at the venue {venue} .\n\n\n"
                 f"Thank you."),
        'time': formatted_date,
    }
    try:
        post_request = requests.post(
            spring_uri,
            params=body_data,
            timeout=5
        )
        response_dict = post_request.json()
        if post_request.status_code==200:
            http_response = HttpResponse(
                post_request.content,
                content_type='application/json',
            )
            print(f"DEBUG: Microservice Response: {response_dict}")
            return response_dict.get('taskID')
    except Exception as e:
        print(f' having problem {e}')
    return None

def turnOffNotifiation(notification_id):
    spring_uri = os.getenv("SPRING_URI_CANCEL")
    body_data = {
        "taskID":notification_id
    }
    try:
        post_request = requests.post(
            spring_uri,
            params=body_data,
            timeout=5
        )
        response_dict = post_request.text
        if post_request.status_code == 200:
            http_response = HttpResponse(
                post_request.content,
                content_type='application/json',
            )
            print(f"DEBUG: Microservice Response: {response_dict}")
            return http_response
    except requests.exceptions.ConnectionError:
        return HttpResponse(
            "Email Service Unavailable, Please try again later.",
            status=503
        )
    return None

@role_required(allowed_roles=['Admin'])
def event_notification(request,id):
    event = Events.objects.get(id=id)
    registered = event.registrations.all().select_related('student')
    if request.method == 'POST':
        if event.reminder_sent:
            event.reminder_sent = False
            event_notification = Notifications.objects.filter(event_id=event.id)
            for entry in event_notification:
                turnOffNotifiation(entry.notification_id)
            event_notification.delete()
            messages.info(request, f"Notification Deactivated Successfully for the event -- {event.title} .")
        else:
            if registered.exists():
                activated_count = 0
                event.reminder_sent = True
                for students in registered:
                    objs = students.student
                    notification_id=turnOnNotification(
                        eventTime= event.date,
                        eventName= event.title,
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
                        activated_count +=1
                messages.success(request, f"Notification Activated Successfully for the event -- {event.title} .")
            else:
                messages.info(request, f"No registered student found for the event {event.title}")

        event.save()
        return redirect('event_lists')
    return render(request,'PushNotification.html',{'events':event})