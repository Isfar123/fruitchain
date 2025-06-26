from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from .models import CustomUser

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            user_type = request.POST['user_type']

            # Validation
            if not username or not password1 or not password2 or not user_type:
                messages.error(request, 'All fields are required')
                return redirect('register')

            if password1 != password2:
                messages.error(request, 'Passwords do not match')
                return redirect('register')

            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('register')

            # Create user
            user = CustomUser.objects.create_user(
                username=username,
                password=password1,
                is_admin=(user_type == 'admin')
            )

            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')

        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
            return redirect('register')

    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            
            if user.is_admin:
                return redirect('admin_dashboard')
            else:
                return redirect('vendor_dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
            
    return render(request, 'login.html')

@login_required
def admin_dashboard(request):
    if not request.user.is_admin:
        messages.error(request, 'Access denied')
        return redirect('vendor_dashboard')
    return render(request, 'admin_dashboard.html')

@login_required
def vendor_dashboard(request):
    return render(request, 'vendor_dashboard.html')

@login_required
def profile(request):
    template = 'profile.html' if request.user.is_admin else 'profile_vendor.html'
    return render(request, template)

@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    return redirect('profile')

@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect!')
            return redirect('profile')

        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match!')
            return redirect('profile')

        request.user.set_password(new_password)
        request.user.save()
        messages.success(request, 'Password changed successfully! Please login again.')
        return redirect('login')
    return redirect('profile')

@login_required
def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        auth_logout(request)
        user.delete()
        messages.success(request, 'Your profile has been deleted.')
        return redirect('home')
    return redirect('profile')

def logout(request):
    auth_logout(request)
    # messages.success(request, 'Logged out successfully')
    return redirect('home')
