from django.urls import path
from . import views
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('confirm/<int:status_id>/', views.confirm, name='confirm'),
    path('cancel/<int:status_id>/', views.cancel, name='cancel'),
    path('completed/<int:status_id>/', views.completed, name='completed'),
    path('view_appointments/', views.view_appointments, name='view_appointments'),
    path('complete_doctor_profile/', views.complete_doctor_profile, name='complete_doctor_profile'),
    path('complete_patient_profile/', views.complete_patient_profile, name='complete_patient_profile'),
    path('patients/', views.view_patients, name='patients'),
]