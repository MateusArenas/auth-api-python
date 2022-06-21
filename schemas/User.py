from mongoengine import *
import bcrypt

from datetime import datetime, timedelta

class _Document(Document):
    meta = { 
        'collection': 'User', 
        'allow_inheritance': True, 
    }
    
    def save(self, *args, **kwargs):
        if 'password' in self:
            hashed = bcrypt.hashpw(self['password'].encode(), bcrypt.gensalt(rounds=10))
            self.password = hashed.decode()
        
        return super(_Document, self).save(*args, **kwargs)

class User(_Document):
    email = StringField(
        unique=True,
        required=True
    )
    password = StringField(
        max_length=500
    )
    verifiedToken = StringField()
    verified = BooleanField(
        default=False
    )
    expiredAt = DateTimeField(
        default=datetime.utcnow
    )

    meta = { 
        'collection': 'User', 
        'allow_inheritance': True, 
        'index_background': True,
        'index_cls': False,
        'indexes': [{'fields': ['expiredAt'], 'expireAfterSeconds': 86400 }]
    }
    