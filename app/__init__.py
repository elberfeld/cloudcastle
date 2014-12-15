from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import LoginManager
from flaskext.couchdb import CouchDBManager, Document, TextField, DateTimeField, ViewField, paginate
from config import config


bootstrap = Bootstrap()

couchdb_manager = CouchDBManager()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    bootstrap.init_app(app)
    
    from models import User, Talk
    couchdb_manager.add_document(User)
    couchdb_manager.add_document(Talk)
    couchdb_manager.setup(app)
    couchdb_manager.sync(app)
    
    login_manager.init_app(app)

    from .talks import talks as talks_blueprint
    app.register_blueprint(talks_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
