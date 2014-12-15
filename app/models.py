from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from flaskext.couchdb import Document, TextField, DateTimeField, ViewField, paginate
from . import login_manager


class User(UserMixin, Document):
    doc_type = 'user'
    
    email = "aaa@bbb.cc" 
    username = "test" 
    is_admin = True
    password_hash = ""
    name = "Test User"

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        password = "test"

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Talk(Document):
    doc_type = 'talk'
    
    title = TextField()
    description = TextField()

    all = ViewField('guestbook', '''
        function (doc) {
            if (doc.doc_type == 'talk') {
                emit(doc.time, doc);
            };
        }''', descending=True)
 
    
    