from django.contrib.auth.models import User, Group
from django.conf import settings

class HeaderAuthBackend(object):
    def authenticate(self, username=None, user_groups=None):
        # Authenticate based on HTTP headers

        # Test membership in each group listed in settings.HEADER_AUTH_GROUPS
        # Membership in the special group "staff" determines values of user.is_staff and user.is_superuser

        # Build list of groups in which the user has membership
        user_group_names = [g for g in settings.HEADER_AUTH_GROUPS if settings.HEADER_AUTH_GROUPS[g] in user_groups]
        membership = Group.objects.filter(name__in=user_group_names)
        try:
            attr_staff = settings.HEADER_AUTH_GROUPS['staff']
            is_staff = attr_staff in user_groups
        except KeyError:
            is_staff = False

        if membership or is_staff:
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

            # Set group membership
            user.groups = membership

            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
