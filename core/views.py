from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Appointment, Doctor, Patient, Department
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    doctors = Doctor.objects.all()[:4]
    return render(request, 'home.html', {'doctors': doctors})

@login_required
def appointment(request):
    departments = Department.objects.all()
    doctors = Doctor.objects.all()

    if request.method == 'POST':
        # Process appointment form data here
        department_id = request.POST.get('department')
        doctor_id = request.POST.get('doctor')
        appointment_date = request.POST.get('date')
        appointment_time = request.POST.get('time')
        reason = request.POST.get('reason')
        # You would typically save this data to the database
        if not doctor_id:
            messages.error(request, "Please select a doctor")
        else:
            patient = request.user.patient
            department = get_object_or_404(Department, id=department_id)
            doctor = get_object_or_404(Doctor, id=doctor_id)

        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            reason=reason
        )
        messages.success(request, "Your appointment has been booked successfully.")
        return redirect('view_appointments')
    context = {
            'departments': departments,
            'doctors':doctors,
    }
    
    return render(request, 'appointment.html', context)


def get_doctors(request, dept_id):
    try:
        doctors = Doctor.objects.filter(department_id=dept_id).values(
            'id', 
            'user__first_name', 
            'user__last_name'
        )

        doctors_list = [
            {
                "id": doc["id"],
                "name": f"{doc['user__first_name']} {doc['user__last_name']}"
            }
            for doc in doctors
        ]

        return JsonResponse({'doctors': doctors_list})

    except Exception as e:
        # This helps debug by returning an error message
        return JsonResponse({'error': str(e)}, status=500)
    
def user_dashboard(request):
    return render(request, 'user-dashboard.html')


def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def doctors(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctors.html', {'doctors': doctors})