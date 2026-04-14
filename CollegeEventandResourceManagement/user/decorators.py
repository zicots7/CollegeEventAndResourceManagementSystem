from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps


def role_required(allowed_roles=[]):
    '''
      1. Check authentication
     2. Check if user's role is in the permitted list
     We also allow 'Admin' by default for most staff actions
   3. If not authorized, send to login or an 'Access Denied' page
    :param allowed_roles: Admin, Student , Faculty
    :return:
    '''
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('userLogin')
            if request.user.role in allowed_roles or request.user.role == 'Admin':
                return view_func(request, *args, **kwargs)
            messages.error(request, "You do not have permission to access this page.")
            return redirect('userLogin')
        return wrapper
    return decorator