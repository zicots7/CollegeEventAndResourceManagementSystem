from django.shortcuts import (
    redirect,
    render
)
from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login,
    logout
)
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import(
    login,
    get_user_model
)
from .decorators import *
from .form import *
User = get_user_model()
def redirect_dashboard(request):
    """
        helper function to avoid showing login page once user already logged in .
    :param request: takes currently logged-in user details
    :return: return to dashboard of users based on thier roles
    """
    user = request.user
    if user.role == 'Admin':
        return redirect('admin_dashboard')
    elif user.role == 'Faculty':
        return redirect('faculty_dashboard')
    elif user.role == 'Student':
        return redirect('student_dashboard')
    else:
        return redirect('userLogin')
@role_required(allowed_roles=['Admin'])
def AddFaculty(request):
    if request.method == 'POST':
        form = FacultyCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'Faculty'
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(form.cleaned_data['password'])
            else:
                user.set_password('faculty@123')
            user.save()
            messages.success(
            request,
                f"Faculty Account -- {user.username} -- has been Created"
            )
            return redirect('faculty_list')
    else:
        form = FacultyCreationForm()
    return render(request,'AddFaculty.html',{'form':form})
@role_required(allowed_roles=['Admin'])
def EditFaculty(request,id):
    faculty = User.objects.get(id=id)
    if request.method == "POST":
        form = StudentCreationForm(request.POST, instance=faculty)
        if form.is_valid():
            form.save()
            # updating existing faculty fields separately
            if form.cleaned_data.get('username'):
                faculty.username = form.cleaned_data['username']
                password = form.cleaned_data.get('password')
            if password:
                faculty.set_password(password)
            else:
                faculty.set_password('faculty@123')
            faculty.save()
            messages.success(
                request,
                f"Faculty Account -- {faculty.username} -- has been Updated."
            )
            return redirect('faculty_list')
    else:
        form = StudentCreationForm(instance=faculty)
        form.fields['username'].initial = faculty.username
        form.fields['password'].initial = ''
    return render(request, 'EditFaculty.html', {'form': form, 'user': faculty})
@role_required(allowed_roles=['Admin'])
def DeleteFaculty(request,id):
    faculty = User.objects.get(id=id)
    if request.method == "POST":
        faculty =User.objects.get(id=id)
        faculty.delete()
        messages.warning(
            request,
            f"Faculty Account -- {faculty.username} -- has been Successfully Deleted."
        )
        return redirect('faculty_list')
    return render(request,'DeleteFaculty.html',{'faculty':faculty})
@role_required(allowed_roles=['Admin'])
def faculty_list(request):
    faculty_list  = User.objects.filter(role='Faculty')
    context = {'faculty':faculty_list}
    return render(request,'FacultyList.html',context)
@role_required(allowed_roles=['Admin'])
def AddStudent(request):
    if request.method == 'POST':
        form = StudentCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'Student'
            password = form.cleaned_data.get('password')
            if password:
                user.set_password('password')
            else:
                user.set_password('student@123')
            user.save()
            messages.success(
                request,
                f"Student Account -- {user.username} -- has been Created."
            )
            return redirect('student_list')
    else:
        form = StudentCreationForm()
    return render(request,'AddStudent.html',{'form':form})
@role_required(allowed_roles=['Admin'])
def EditStudent(request,id):
    student = User.objects.get(id=id)
    if request.method == "POST":
        form = StudentCreationForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            if form.cleaned_data.get('username'):
                student.username = form.cleaned_data.get('username')
                password=form.cleaned_data.get('password')
            if password:
                student.set_password(password)
            else:
                student.set_password('student@123')
            student.save()
            messages.success(
                request,
                f" Student Account -- {student.username} -- has been Updated."
            )
            return redirect('student_list')
    else:
        form = StudentCreationForm(instance=student)
        form.fields['username'].initial = student.username
        form.fields['password'].initial = ''  # not pre-filling password for security reasons
    return render(request, 'EditStudent.html', {'form': form, 'user': student})

@role_required(allowed_roles=['Admin'])
def DeleteStudent(request,id):
    student = User.objects.get(id=id)
    if request.method == "POST":
        student = User.objects.get(id=id)
        student.delete()
        messages.warning(
            request,
            f"Student Account -- {student.username} -- has been Successfully Deleted."
        )
        return redirect('student_list')
    return render(request, 'DeleteStudent.html', {'student': student})
@role_required(allowed_roles=['Admin'])
def student_list(request):
    student_list = User.objects.filter(role='Student')
    context = {'students':student_list}
    return render(request,'StudentList.html',context)
def userLogin(request):
    if request.user.is_authenticated:
        return redirect_dashboard(request)
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(
                username=username,
                password=password
            )
            if user:
                login(request,user)
                if user.role == 'Admin':
                    return redirect('admin_dashboard')
                elif user.role == 'Faculty':
                    return redirect('faculty_dashboard')
                else:
                    return redirect('student_dashboard')
    else:
        form = AuthenticationForm()
    return render(request,'UserLogin.html',{'form':form})
def userLogout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('userLogin')
    return redirect('userLogin')
