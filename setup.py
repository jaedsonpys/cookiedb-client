from setuptools import setup

setup(
    name='cookiedb-client',
    description='A client for manipulating CookieDB Server databases.',
    version='0.1.0',
    author='Jaedson Silva',
    author_email='imunknowuser@protonmail.com',
    packages=['cookiedbclient'],
    install_requires=['requests==2.28.1']
)
