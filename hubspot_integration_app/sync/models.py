from datetime import datetime, timedelta
from mongoengine import Document, StringField, DateTimeField, IntField


class Token(Document):
    user = StringField()
    access_token = StringField()
    refresh_token = StringField()
    expires_in = IntField()
    created = DateTimeField(default=datetime.now)

    def is_expired(self):
        return datetime.now() >= self.created + timedelta(seconds=self.expires_in)
