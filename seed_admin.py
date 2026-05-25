import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulsenotify.settings.local')
django.setup()

from django.contrib.auth.models import User
from pulse.models import UserProfile

def seed():
    user, created = User.objects.get_or_create(username='admin', email='admin@example.com')
    user.set_password('adminpass')
    user.save()
    profile, _ = UserProfile.objects.get_or_create(user=user)
    profile.role = UserProfile.Role.ADMIN
    profile.save()
    print("Successfully seeded admin user with username 'admin' and password 'adminpass'.")


if __name__ == '__main__':
    seed()
