from setuptools import setup, find_packages
from sys import version_info

from ntfy import __version__


deps = ['requests', 'ruamel.yaml', 'appdirs']
extra_deps = {
    ':sys_platform == "win32"': ['pypiwin32==219'],
    'xmpp': [
        'sleekxmpp', 'dnspython' if version_info[0] < 3 else 'dnspython3'],
    'emoji': ['emoji'],
    'pid':['psutil'],
}
test_deps = ['mock', 'sleekxmpp', 'emoji', 'psutil']


setup(
    name='ntfy',

    version=__version__,

    description='A utility for sending push notifications',

    url='https://github.com/dschep/ntfy',

    author='Daniel Schep',
    author_email='dschep@gmail.com',

    license='GPLv3',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',

        'Environment :: Console',

        'Intended Audience :: End Users/Desktop',

        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='push notification',

    packages=find_packages(exclude=['tests', 'tests.*']),
    package_data={'ntfy': ['icon.png', 'icon.ico', 'shell_integration/*.sh']},

    install_requires=deps,

    extras_require=extra_deps,

    tests_require=test_deps,
    test_suite='tests',

    entry_points={
        'console_scripts': [
            'ntfy = ntfy.cli:main',
        ],
    },
)
