from django.contrib import messages
from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from core.models import Appointment, Doctor, Department, Patient
from django.utils import timezone
User = get_user_model()

# Create your views here.
@login_required
def dashboard(request):
    user = request.user
    context = {}

    if user.role == 'doctor':
        try:
            doctor = Doctor.objects.get(user=user)
        except Doctor.DoesNotExist:
            return redirect('complete_doctor_profile')
        appointments = Appointment.objects.filter(doctor=doctor, appointment_date__gte=timezone.now()).order_by('appointment_date', 'appointment_time')
        context['pending_appointments'] = appointments.filter(status='pending')
        context['upcoming_appointments'] = appointments.filter(status='confirmed')
        context['today_appointments'] = appointments.filter(status='confirmed', appointment_date=timezone.now().date())
        context['appointments'] = appointments  # keep for compatibility
        return render(request, 'doctor_dashboard.html', context)

    elif user.role == 'patient':
        if not hasattr(user, 'patient'):
            return redirect('complete_patient_profile')
        appointments = Appointment.objects.filter(patient__user=user, appointment_date__gte=timezone.now()).order_by('appointment_date', 'appointment_time')
        context['next_appointment'] = appointments.first()  # Get the next appointment
        context['appointments'] = appointments
        return render(request, 'user-dashboard.html', context)

    else:
        return redirect('home')
@login_required  
def complete_doctor_profile(request):
    user = request.user
    departments = Department.objects.all()
    if request.method == 'POST':
        department_id = request.POST.get('department')
        photo = request.FILES['photo']
        specialization = request.POST.get('specialization')
        experience = request.POST.get('experience')

        if user.role != 'doctor':
            messages.error(request, "Invalid role for completing doctor profile.")
            return redirect('dashboard')
        doctor = Doctor.objects.create(
            user=request.user,
            department_id=department_id,
            photo=photo,
            specialization=specialization,
            experience_years=experience
        )
        return redirect('dashboard')
    return render(request, 'complete_doctor_profile.html', {'departments': departments})

@login_required
def complete_patient_profile(request):
    user = request.user
    if request.method == 'POST':
        date_of_birth = request.POST.get('date_of_birth')
        blood_group = request.POST.get('blood_group')
        age = request.POST.get('age')
        emergency_contact = request.POST.get('emergency_contact')

        # Update existing patient profile instead of creating new one
        if user.role != 'patient':
            messages.error(request, "Invalid role for completing patient profile.")
            return redirect('dashboard')
        patient, created = Patient.objects.get_or_create(user=request.user)
        patient.date_of_birth = date_of_birth
        patient.blood_group = blood_group
        patient.age = age
        patient.emergency_contact = emergency_contact
        patient.save()

        return redirect('dashboard')
    return render(request, 'complete_patient_profile.html')



def confirm(request, status_id):
    appointment = Appointment.objects.get(id=status_id)
    appointment.status = 'confirmed'
    appointment.save()
    return dashboard(request)

def cancel(request, status_id):
    appointment = Appointment.objects.get(id=status_id)
    appointment.status = 'cancelled'
    appointment.save()
    return dashboard(request)
def completed(request, status_id):
    appointment = Appointment.objects.get(id=status_id)
    appointment.status = 'completed'
    appointment.save()
    return dashboard(request)

@login_required
def view_appointments(request):
    user = request.user
    all_appointments = Appointment.objects.filter(patient__user=user).order_by('-created_at')
    
    upcoming_appointments = all_appointments.filter(status__in=['pending', 'confirmed'])
    past_appointments = all_appointments.filter(status__in=['completed', 'cancelled'])
    
    return render(request, 'view_appointments.html', {
        'upcoming_appointments': upcoming_appointments,
        'past_appointments': past_appointments
    })


def view_patients(request):
    user = request.user
    try:
        doctor = Doctor.objects.get(user=user)
    except Doctor.DoesNotExist:
        return redirect('complete_profile')
    
    appointments = Appointment.objects.filter(doctor=doctor).select_related('patient__user')
    patient_ids = appointments.values_list('patient_id', flat=True).distinct()
    patients = Patient.objects.filter(id__in=patient_ids)
    
    return render(request, 'view_patients.html', {'patients': patients})