from django.urls import path
from . import views
from .views import get_doctors

urlpatterns = [
    path('', views.home, name='home'),
    path('appointment/', views.appointment, name='appointment'),
    path('get-doctors/<int:dept_id>/', get_doctors, name='get_doctors'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('doctors/', views.doctors, name='doctors'),
]

