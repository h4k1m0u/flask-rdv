#!/usr/bin/python
from peewee import MySQLDatabase, Model, CharField, DateTimeField 
from datetime import datetime

# database
database = MySQLDatabase('flask', host='localhost', user='root', passwd='toor')

def create_tables():
    database.connect()
    User.create_table()

class BaseModel(Model):
    class Meta:
        database = database

class User(BaseModel):
    username = CharField()    
    email = CharField()
    password = CharField()
    created_at = DateTimeField(default=datetime.now)
