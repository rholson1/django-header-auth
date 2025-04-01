
import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-header-auth',
    version='0.6',
    packages=['header_auth'],
    include_package_data=True,
    install_requires=['django'],
    license='BSD License',
    description='A simple Django app to enable authentication and authorization based on HTTP headers.',
    long_description=README,
    url='https://github.com/rholson1/django-header-auth',
    author='Rob Olson',
    author_email='rolson@waisman.wisc.edu',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)