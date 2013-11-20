from django.contrib.auth.models import User
from django.conf import settings

class HeaderAuthBackend(object):
    def authenticate(self, username=None, user_groups=None):
        # Authenticate based on HTTP headers
        
        attr_staff = settings.HEADER_AUTH_GROUPS['staff']
        attr_user = settings.HEADER_AUTH_GROUPS['users']
        is_user = attr_user in user_groups
        is_staff = attr_staff in user_groups
        if is_user or is_staff:
            try:
                user = User.objects.get(username=username)
                # Update staff status in case manifest group membership changed.
                user.is_staff = is_staff
                user.is_superuser = is_staff
                user.save()
            except User.DoesNotExist:
                # Create a new user.  The password can be set to anything
                # because it isn't used.
                user = User(username=username, password='fakepassword')
                user.is_staff = is_staff
                user.is_superuser = is_staff
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

                
