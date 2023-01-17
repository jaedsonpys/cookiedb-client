from setuptools import setup

with open('README.md', 'r') as reader:
    readme = reader.read()

setup(
    name='cookiedb-client',
    description='A client for manipulating CookieDB Server databases.',
    long_description=readme,
    long_description_content_type='text/markdown',
    version='0.1.0',
    author='Jaedson Silva',
    author_email='imunknowuser@protonmail.com',
    packages=['cookiedbclient'],
    url='https://github.com/jaedsonpys/cookiedb-client',
    project_urls={
        'License': 'https://github.com/jaedsonpys/cookiedb-client/blob/master/LICENSE',
    },
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Database :: Database Engines/Servers'
    ],
    keywords=['database', 'server', 'noSQL', 'cookiedb']
)
