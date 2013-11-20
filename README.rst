===========
Header_Auth
===========

Header_Auth is a simple Django app that adds support for authentication and authorization via HTTP headers.  It is
designed to worth with the NetID login service and Manifest group management service at UW-Madison.


Quick start
-----------

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


