import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "showmax.showmax.settings")
django.setup()

from django.contrib.auth.models import User

# Create user


user = User(username='user', password='password')
try:
    user.save()
except Exception:
    pass  # User exist
