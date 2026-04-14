from django.shortcuts import render,redirect
from user.decorators import (
role_required
)

def dashboard_redirect(request):
    user = request.user
    if user.role == 'Admin':
        return redirect('admin_dashboard')
    elif user.role == 'Faculty':
        return redirect('faculty_dashboard')
    elif user.role == 'Student':
        return redirect('student_dashboard')
    else:
        return redirect('userLogin')  # fallback
@role_required(allowed_roles=['Admin'])
def adminDashboard(request):
    return render(request,'admin_dashboard.html')
@role_required(allowed_roles=['Faculty'])
def facultyDashboard(request):
    return render(request,'faculty_dashboard.html')

@role_required(allowed_roles=['Student'])
def studentDashboard(request):
    return render(request,'student_dashboard.html')

