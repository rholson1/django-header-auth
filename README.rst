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

    def logout_view(http_request):
        logout(http_request)  # log out of local session
        return redirect(getattr(settings, 'LOGOUT_URL'))  # log out of login server

where I have defined the LOGOUT_URL setting as::

    LOGOUT_URL = "/Shibboleth.sso/Logout?return=https://login.wisc.edu/logout"