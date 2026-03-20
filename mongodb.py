from pymongo import MongoClient
from datetime import datetime, timezone


MONGO_URI = 'mongodb://localhost:27017/'
DB_NAME = 'monoFlask_AI'

def mongoConnect():
    client = MongoClient(MONGO_URI)
    try:
        db = client[DB_NAME]
        collection = db.monoflask_collection

        #insert/create one document
        document = {
            'name': 'sample',
            'creted at': datetime.now(),
            'data': {
                'full name': 'name',
                'email': 'mail'
            }

        }
        result = collection.insert_one(document)
        print(f'inserted document ID: {result.inserted_id}')
    
        #to search/retrive saved documents
        find_document= collection.find({'name': 'sample'})
        for document in find_document:
            print(f'Found document: {document}')  
    
        #to update saved documents
        update_document= collection.update_one(
            {'name': 'sample'},
            {'$set': {'data.full name': 'somto'}}
            ) 

        print(f'modified {update_document.modified_count} document(s)')
  
        #to delete documents
        delete_document= collection.delete_one({'name': 'sample'})        
        print(f'deleted {delete_document.deleted_count} document(s)')

    except Exception as e:
        print(f'mongoerror: {str(e)}') 

    finally:
        client.close() 
