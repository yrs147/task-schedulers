from peewee import Model,AutoField, CharField, DateTimeField, MySQLDatabase

db = MySQLDatabase('mydb', user='root', password='test', host='mysql-service', port=3306)

class Task(Model):
    id = AutoField(primary_key=True)
    name = CharField()
    execution_time = DateTimeField()
    status = CharField(default='pending')
    cron_schedule = CharField(null=True)
    recurring = CharField(default='no')

    class Meta:
        database = db

db.connect()


db.create_tables([Task])


db.close()