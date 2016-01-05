from setuptools import setup
from sys import platform

deps = ['requests']

if platform == 'win32':
    deps.append('pypiwin32')

setup(
    name='ntfy',

    version='0.2.1',

    description='A utility for sending push notifications',

    url='https://github.com/dschep/ntfy',

    author='Daniel Schep',
    author_email='dschep@gmail.com',

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',

        'Environment :: Console',

        'Intended Audience :: End Users/Desktop',

        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='push notification',

    packages=['ntfy', 'ntfy.backends'],
    package_data={'ntfy': ['icon.png', 'icon.ico']},

    install_requires=deps,

    entry_points={
        'console_scripts': [
            'ntfy = ntfy.cli:main',
        ],
    },
)
