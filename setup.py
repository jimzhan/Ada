# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


packages  = find_packages()
namespace = packages[0]


setup(
    name = namespace,
    version = __import__(namespace).get_version(),
    url = 'https://github.com/jimzhan/rex',
    author = 'Jim Zhan',
    author_email = 'jim.zhan@me.com',
    packages = find_packages(),
    description = 'A high-level Python Tools Set.',

    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    entry_points = {
        'console_scripts': [
        ]
    },
    install_requires=[
        'clint >= 0.3.1',
        'Unidecode >= 0.04.9',
    ],

)
