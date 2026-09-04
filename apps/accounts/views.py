from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

import re
from django.contrib.auth import update_session_auth_hash



def register(request):
    if request.method == 'POST':
        _name = request.POST.get('name')
        _email = request.POST.get('email')
        _password = request.POST.get('password')
        _confirm_password = request.POST.get('confirm_password')

        _username = _email

        if _password != _confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'auth/register.html')

        password_error = get_password_strength_error(_password)
        if password_error:
            messages.error(request, password_error)
            return render(request, 'auth/register.html')

        if User.objects.filter(username=_username).exists():
            messages.error(request, "A user with this email/username already exists.")
            return render(request, 'auth/register.html')

        if User.objects.filter(email=_email).exists():
            messages.error(request, "This email is already registered.")
            return render(request, 'auth/register.html')

        User.objects.create_user(
            first_name=_name,
            username=_username,
            email=_email,
            password=_password
        )
        messages.success(request, "Registration successful! Please login.")
        return redirect('accounts:login_view')

    return render(request, 'auth/register.html')


def get_password_strength_error(password):

    """
    Returns an error message string if the password does not meet strength
    requirements, or None if it passes. Requirements:
      - at least 8 characters
      - at least one uppercase letter
      - at least one digit
      - at least one special character
    """

    if not password or len(password) < 8:
        return "Password must be at least 8 characters long."

    if not re.search(r'[A-Z]', password):
        return "Password must contain at least one uppercase letter."

    if not re.search(r'[0-9]', password):
        return "Password must contain at least one number."

    if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\];\'`~/\\]', password):
        return "Password must contain at least one special character."

    return None
            



def login_view(request):
    if request.method == 'POST':
        _username = request.POST.get('email')
        _password = request.POST.get('password')
        
        user = authenticate(request, username=_username, password=_password)

        if user is not None:
            login(request, user)
            return redirect('user:user_home')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('accounts:login_view') 
            
    return render(request, 'auth/login.html')



@login_required(login_url='login_view')
def logout_view(request):
    django_logout(request) 
    return redirect('accounts:login_view')


@login_required(login_url='login_view')
def change_password(request):
    if request.method == 'POST':
        _current_password = request.POST.get('current_password')
        _new_password = request.POST.get('new_password')
        _confirm_password = request.POST.get('confirm_password')
 
        user = request.user
 
        if not user.check_password(_current_password):
            messages.error(request, "Current password is incorrect.")
            return render(request, 'auth/change_password.html')
 
        if _new_password != _confirm_password:
            messages.error(request, "New passwords do not match.")
            return render(request, 'auth/change_password.html')
 
        if _new_password == _current_password:
            messages.error(request, "New password must be different from your current password.")
            return render(request, 'auth/change_password.html')
 
        password_error = get_password_strength_error(_new_password)
        if password_error:
            messages.error(request, password_error)
            return render(request, 'auth/change_password.html')
 
        user.set_password(_new_password)
        user.save()
 
        update_session_auth_hash(request, user)
 
        messages.success(request, "Your password has been changed successfully.")
        return redirect('user:user_home')
 
    return render(request, 'auth/change_password.html')
