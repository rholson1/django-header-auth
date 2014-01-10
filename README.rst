===========
Header_Auth
===========

Header_Auth is a simple Django app that adds support for authentication and authorization via HTTP headers.  It is
designed to work with the NetID login service and Manifest group management service at UW-Madison.


Installation
------------

pip install https://bitbucket.org/waismanctc/django-header-auth/get/tip.tar.gz


Required Settings
-----------------

1. Enable the backend::

    AUTHENTICATION_BACKENDS = (
        'header_auth.backends.HeaderAuthBackend',
    )

2. Add the HeaderAuthMiddleware after the AuthenticationMiddleware (add if not present)::

    MIDDLEWARE_CLASSES = (
        ...
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'header_auth.middleware.HeaderAuthMiddleware',
        ...
    )

3. Specify HTTP headers used for authentication and authorization::

    HEADER_AUTH_MAP = {
        'user': 'REMOTE_USER',
        'groups': 'isMemberOf'
    }

4. Specify names of authorization groups::

    HEADER_AUTH_GROUPS = {
        'users': 'uw:domain:ctc.waisman.wisc.edu:registry_users',
        'staff': 'uw:domain:ctc.waisman.wisc.edu:registry_staff'
    }



Logging Out
-----------

Logging out of the application requires both a logout of the local session and a logout of the login server.
I use a logout view::

    from django.contrib.auth import logout
    from django.conf import settings
    from django.shortcuts import redirect

    def logout_view(http_request):
        logout(http_request)  # log out of local session
        return redirect(getattr(settings, 'LOGOUT_URL'))  # log out of login server

where I have defined the LOGOUT_URL setting as::

    LOGOUT_URL = "/Shibboleth.sso/Logout?return=https://login.wisc.edu/logout"


Authorization Groups
--------------------

The groups listed in HEADER_AUTH_GROUPS will be created if they do not already exist.  When a user logs in, group
membership will be set for each group identifier provided in the appropriate HTTP header.  Any other group membership
relations will be cleared.  Membership in the special group "staff" is used to set values of user.is_staff and
user.is_superuser.

One way to use group membership to control access to views is using the @user_passes_test decorator::

    @login_required
    @user_passes_test(lambda u: u.is_staff)
    def my_view(request):
        """A sample view that only staff can access."""
        # ...

Or you could define a test function::

    def is_student(user):
        """Use with user_passes_test decorator to limit access to authenticated members of 'students' group"""
        return user.is_authenticated() and user.groups.filter(name='students').exists()

    @user_passes_test(is_student)
    def student_view(request):
        """A sample view that only students can access."""
        # ...
