from peewee import *
import os
db_path = '/app/db/ss.db'
#db_path = '/home/dan/coding/python/SwampScanner/app/db/ss.db'

if not os.path.exists(db_path):
  raise FileNotFoundError(f"Database file not found at {db_path}")
db = SqliteDatabase(db_path)

class BaseModel(Model):
  class Meta:
    database = db
        
class TargetPage(BaseModel):
  page_url = TextField(unique=True)
  element_match = TextField()
    
class PageRequestHeader(BaseModel):
  header_key = TextField()
  header_value = TextField()
  page = ForeignKeyField(TargetPage)

class Advert(BaseModel):
  url = TextField(unique=True)
  description = TextField()
  page = ForeignKeyField(TargetPage)