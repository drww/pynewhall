try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'PyNewhall',
    'author': 'Drew Waltman',
    'url': 'github.com/drww/pynewhall',
    'download_url': 'github.com/drww/pynewhall',
    'author_email': '',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['pynewhall'],
    'scripts': [],
    'name': 'pynewhall'
}

setup(**config)
