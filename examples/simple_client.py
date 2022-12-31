from cookiedbclient import CookieDBClient

db = CookieDBClient('http://127.0.0.1:5500')

# Use this code snippet to register a account:
# db.register('example', 'example@cookiedb.com', '1234')

db.login('example@cookiedb.com', '1234')

db.create_database('languages', if_not_exists=True)
db.open('languages')

data = {}

while True:
    print('-' * 20)
    print('Add languages to database (999 in "name" to list):')
    print('-' * 20)

    name = input('Name: ')

    if name == '999':
        break

    author = input('Author: ')
    creation_date = input('Creation date: ')
    extension = input('Extension: ')

    confirm = input('\nAdd this language? [y/n]: ').strip()
    confirm = confirm.lower()

    while confirm not in ('y', 'n'):
        print('Invalid option, please repeat.')
        confirm = input('Add this language? [y/n]: ').strip()
        confirm = confirm.lower()

    if confirm == 'y':
        language = {
            'name': name,
            'author': author,
            'creation_date': creation_date,
            'extension': extension
        }

        db.add(f'languages/{name}', language)


print('-' * 20)
print('All languages added')
print('-' * 20)

print(db.get('languages'))