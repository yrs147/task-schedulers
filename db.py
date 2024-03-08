from peewee import Model, CharField, DateTimeField, MySQLDatabase

db = MySQLDatabase('mydb', user='root', password='test', host='localhost', port=3306)

class Task(Model):
    name = CharField()
    execution_time = DateTimeField()
    recurring_type = CharField(null=True)
    recurring_value = CharField(null=True)

    class Meta:
        database = db

db.connect()
db.create_tables([Task])