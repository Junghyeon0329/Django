from datetime import timedelta
from django.utils import timezone
from .models import PasswordHistory

def is_password_expired(user):
    
    password_expiry_duration = timedelta(days=30)    
    latest_password_history = PasswordHistory.objects.filter(user=user).order_by('-password_changed_at').first()
    
    if not latest_password_history:
        PasswordHistory.objects.create(user=user, password_changed_at=user.timezone.now())
        return False
    
    if timezone.now() - latest_password_history.password_changed_at > password_expiry_duration:
        return True

    return False
