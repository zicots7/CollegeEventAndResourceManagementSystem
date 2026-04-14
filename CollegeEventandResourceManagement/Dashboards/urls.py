from django.urls import path,include
from . import views

urlpatterns = [
    path('admin/',views.adminDashboard,name='admin_dashboard'),
    path('student/',views.studentDashboard,name='student_dashboard'),
    path('faculty/',views.facultyDashboard,name='faculty_dashboard'),
]