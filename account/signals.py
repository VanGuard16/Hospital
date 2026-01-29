from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from core.models import User, Patient, Doctor
@receiver(post_save, sender=User)
def ensure_patient_profile(sender, instance, **kwargs):
    if instance.role == 'patient':
        Patient.objects.get_or_create(user=instance)


@receiver(pre_save, sender=User)
def handle_role_change(sender, instance, **kwargs):
    if not instance.pk:
        return
    
    previous = User.objects.get(pk=instance.pk)

    if previous.role == 'patient' and instance.role == 'doctor':
        Patient.objects.filter(user=instance).delete()