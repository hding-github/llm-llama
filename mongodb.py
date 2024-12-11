import asyncio
import os
from dotenv import load_dotenv
load_dotenv()
MONGODB_CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")

import time
from pymongo import MongoClient
class MongoDB_Atlas_Client ():
  def __init__ (self, altas_uri = MONGODB_CONNECTION_STRING, dbname = MONGODB_DATABASE):
    print("*** MongoDB_Atlas_Client ***")
    print(" len (altas_uri) = " + str(len(altas_uri)))
    time_start = time.time()
    self.mongodb_client = MongoClient(altas_uri)
    self.database = self.mongodb_client[dbname]
    time_end = time.time()
    print(time_end - time_start)
    print("*******************")
    print("*")
  def __destroy__(self):
    self.mongodb_client.close()

   ## A quick way to test if we can connect to Atlas instance
  def ping (self):
    result = self.mongodb_client.admin.command('ping')
    return result


  def get_collection (self, collection_name):
    collection = self.database[collection_name]
    return collection

  def find (self, collection_name, filter = {}, limit=0):
    collection = self.database[collection_name]
    items = list(collection.find(filter=filter, limit=limit))
    return items
  
  def find_one (self, collection_name, filter = {}):
    collection = self.database[collection_name]
    items = collection.find_one(filter=filter)
    return items
  
  def find_all (self, coolection_name):
    collection = self.database[coolection_name]
    items = collection.find().to_list(None)
    return items

  def insert_one(self, collection_name, model):
    collection = self.database[collection_name]
    result = collection.insert_one(model.model_dump())
    return result

  def delete_one(self, collection_name, filter):
    collection = self.database[collection_name]
    result = collection.delete_one(filter)
    return result
  
  def update_one(self, collection_name, filter, value_set, limit=0):
    # filter: Updating filter to specify a collection.
    #filter = { 'title': 'ABC' }
    
    # value_set: Values to be updated.
    #newvalues = { "$set": { 'quantity': 25 } }
    newvalues = { "$set": value_set }

    # Using update_one() method for single 
    # updation.
    collection = self.database[collection_name]
    collection.update_one(filter, newvalues) 
    items = list(collection.find(filter=filter, limit=limit))
    return items
    

  






