from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.conf import settings

class HardcodedAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Check against hardcoded credentials from settings
        hardcoded_username = getattr(settings, 'HARDCODED_USERNAME', 'admin')
        hardcoded_password = getattr(settings, 'HARDCODED_PASSWORD', 'admin123')

        if username == hardcoded_username and password == hardcoded_password:
            # Credentials match!
            # Now we need a User object. get_or_create logic ensures it exists.
            # We don't care about the DB password.
            try:
                user, created = User.objects.get_or_create(username=username)
                if created:
                    # Set default attributes for a new admin user
                    user.is_staff = True
                    user.is_superuser = True
                    user.set_unusable_password() # Ensure it can't be logged in via standard auth
                    user.save()
                else:
                    # Ensure existing user has permissions if they were somehow lost
                    if not user.is_staff or not user.is_superuser:
                        user.is_staff = True
                        user.is_superuser = True
                        user.save()
                return user
            except Exception:
                return None
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
