try:
    from setuptools import setup
except:
    from distutils.core import setup


config = {
    'description': 'Basic Budgeting',
    'author': 'Travis Cooper',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'travis@evolvingcoder.com',
    'version': '0.1',
    'install_requires': ['nose', 'webpy'],
    'packages': ['budgetbasic'],
    'scripts': [],
    'name': 'budgetbasic'
}

setup(**config)
