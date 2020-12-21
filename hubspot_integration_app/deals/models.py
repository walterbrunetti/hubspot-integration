from mongoengine import Document, StringField, DateTimeField, IntField, DecimalField


class Deal(Document):
    deal_id = IntField(required=True)
    name = StringField(required=True)
    stage = StringField()
    close_date = DateTimeField()
    deal_type = StringField()
    amount = DecimalField()
