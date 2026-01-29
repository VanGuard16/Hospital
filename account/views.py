from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from core.models import Patient
User = get_user_model()
# Create your views here.
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('register')

        try:
            user = User.objects.create_user(
                username=username, 
                first_name=firstname, 
                last_name=lastname,
                email=email, 
                password=password,
                role='patient')
            
            # Create Patient profile
            Patient.objects.create(user=user)
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Registration failed: {str(e)}")
            return redirect('register')
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(post_login_redirect(user))
        else:
            messages.error(request, "Invalid username or password")
            return render(request, 'login.html')
        
    return render(request, 'login.html')
def logout_view(request):
    logout(request)
    return redirect('login')

def post_login_redirect(user):
    if user.role == 'patient':
        try:
            patient = Patient.objects.get(user=user)
            # Check if essential profile fields are filled
            if not patient.date_of_birth or not patient.emergency_contact:
                return 'complete_patient_profile'
        except Patient.DoesNotExist:
            return 'complete_patient_profile'
    return 'dashboard'