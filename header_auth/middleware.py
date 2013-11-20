from django.contrib import auth
from shib_auth.backends import ShibbolethBackend
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings


class ShibbolethMiddleware(object):
    """ Middleware for providing authentication based on Shibboleth attributes"""

    def process_request(self, request):
        # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The Django Shibboleth auth middleware requires the"
                " authentication middleware to be installed. Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the ShibbolethMiddleware class.")

        try:
            shib_attrs = getattr(settings, 'SHIBBOLETH_ATTRIBUTE_MAP', {'user': 'REMOTE_USER', 'groups': 'isMemberOf'})
            username = request.META[shib_attrs['user']]
            manifest_groups = request.META[shib_attrs['groups']]
        except KeyError:
            # If specified header doesn't exist then remove any existing
            # authenticated remote-user, or return (leaving request.user set to
            # AnonymousUser by the AuthenticationMiddleware).
            if request.user.is_authenticated():
                try:
                    stored_backend = load_backend(request.session.get(
                        auth.BACKEND_SESSION_KEY, ''))
                    if isinstance(stored_backend, ShibbolethBackend):
                        auth.logout(request)
                except ImproperlyConfigured:
                    # backend failed to load
                    auth.logout(request)
 
        # We are seeing this user for the first time in this session, attempt
        # to authenticate the user.
        user = auth.authenticate(username=username, manifest_groups=manifest_groups)
        if user:
            # User is valid. Set request.user and persist user in the session
            # by logging the user in.
            request.user = user
            auth.login(request, user)
