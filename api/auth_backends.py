from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try to authenticate using email
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            try:
                # Try to authenticate using username
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None

        if user.check_password(password):
            return user
        return None