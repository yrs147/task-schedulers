from peewee import Model,AutoField, CharField, DateTimeField, MySQLDatabase

db = MySQLDatabase('mydb', user='root', password='test', host='localhost', port=3306)

class Task(Model):
    id = AutoField(primary_key=True)
    name = CharField()
    execution_time = DateTimeField()

    class Meta:
        database = db

db.connect()


db.create_tables([Task])


db.close()