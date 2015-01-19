#!/usr/bin/env python
import os
if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

from app import create_app
from flask.ext.script import Manager
from app import couchdb_manager
from app.models import User, Talk

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)



@manager.command
def adduser(email, username, admin=False):
    """Register a new user."""
    from getpass import getpass
    password = getpass()
    password2 = getpass(prompt='Confirm: ')
    if password != password2:
        import sys
        sys.exit('Error: passwords do not match.')
    #TODO: create user magic     
    user = User(email=email, username=username, password=password, is_admin=admin)
    print('User {0} was registered successfully.'.format(username))

@manager.command
def addtalk(title, description):
    """Register a new talk."""
    couchdb_manager.request_start()
    talk = Talk(title = title, description = description)
    talk.store()
    print('Talk {0} was registered successfully.'.title)

@manager.command
def listtalks():
    """List all talks """
    couchdb_manager.request_start()
    for talk in Talk.all(): 
        print(talk.title + " " + talk.description)
         
@manager.command
def gettalk(id):
    """Get Talk by ID """
    couchdb_manager.request_start()
    talk = Talk.load(id)
    print(talk.title + " " + talk.description)

if __name__ == '__main__':
    manager.run()

