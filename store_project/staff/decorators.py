from django.shortcuts import redirect

def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')

            if hasattr(request.user, 'staff'):
                if request.user.staff.role in allowed_roles:
                    return view_func(request, *args, **kwargs)

            return redirect('staff_list')  # if unauthorized
        return wrapper
    return decorator
