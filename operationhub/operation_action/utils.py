from datetime import timedelta
from django.utils import timezone

def is_password_expired(user):
    print("도착")
    print(user)
    password_expiry_duration = timedelta(days=30)

    if user.password_changed_at is None:
        user.password_changed_at = timezone.now()
        user.save()

    if timezone.now() - user.password_changed_at > password_expiry_duration:
        return True

    return False
