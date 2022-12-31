from setuptools import setup

with open('README.md', 'r') as reader:
    readme = reader.read()

setup(
    name='cookiedb-client',
    description='A client for manipulating CookieDB Server databases.',
    long_description=readme,
    long_description_content_type='text/markdown'
    version='0.1.0',
    author='Jaedson Silva',
    author_email='imunknowuser@protonmail.com',
    packages=['cookiedbclient'],
    install_requires=['requests==2.28.1']
)
