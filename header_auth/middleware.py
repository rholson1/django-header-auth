from django.contrib import auth
from django.contrib.auth.models import Group
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings


class HeaderAuthMiddleware(object):
    """ Middleware for providing authentication and authorization based on HTTP headers"""

    def __init__(self):
        """ Make sure that groups exist for each member of settings.HEADER_AUTH_GROUPS
        """
        for group in settings.HEADER_AUTH_GROUPS:
            Group.objects.get_or_create(name=group)

    def process_request(self, request):
        # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The Django header auth middleware requires the"
                " authentication middleware to be installed. Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the HeaderMiddleware class.")

        headers = getattr(settings, 'HEADER_AUTH_MAP', {'user': 'REMOTE_USER', 'groups': 'isMemberOf'})

        try:
            header_user = headers['user']
            header_groups = headers['groups']
        except KeyError:
            raise ImproperlyConfigured(
                "The Django header auth middleware requires "
                " the definition of the HEADER_AUTH_MAP dictionary"
                " with keys 'user' and 'groups'. "
            )

        try:
            username = request.META[header_user]
            user_groups = request.META[header_groups]
        except KeyError:
            # authentication headers are not present; do not authenticate
            return

        # If the user is already authenticated and that user matches the user in the headers, then
        # the correct user is already logged in and we don't need to continue.
        if request.user.is_authenticated():
            if request.user.get_username() == username:
                return

        # We are seeing this user for the first time in this session; attempt
        # to authenticate the user.
        user = auth.authenticate(username=username, user_groups=user_groups)
        if user:
            # User is valid. Set request.user and persist user in the session
            # by logging the user in.
            request.user = user
            auth.login(request, user)
