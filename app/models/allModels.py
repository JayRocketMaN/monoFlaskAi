from app.extension import db
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash
from datetime import datetime
import mongoengine


class ChatMessage(db.EmbeddedDocument):
    sender = db.StringField(required=True) # 'user' or 'ai'
    text = db.StringField(required=True)
    timestamp = db.DateTimeField(default=datetime.utcnow)

class ChatSession(db.EmbeddedDocument):
       session_id = db.StringField() 
       title = db.StringField()     
       messages = mongoengine.ListField(mongoengine.EmbeddedDocumentField(ChatMessage)) 

class Users(db.Document, UserMixin):
    fullname= db.StringField(required=True)
    email = db.EmailField(required=True, unique=True)
    username = db.StringField(required=True, unique=True)
    password_hash = db.StringField(required=True)
    all_conversations = mongoengine.ListField(mongoengine.EmbeddedDocumentField(ChatSession))

    def set_password(self, password):
            self.password_hash = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
            return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return str(self.id) 
    
    meta = {
            'collection': 'monoflask_collection',
            'strict': False,  # Prevents crashing on extra DB fields
            'allow_inheritance': False
        }

def __repr__(self):
    return f'<User{self.username}>'

