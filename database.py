from google.cloud import firestore_v1 as firestore
from google.auth import credentials
from google.cloud.firestore_v1 import Increment
import firebase_admin

default_app = firebase_admin.initialize_app()


# Network comms w/ DB
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore

# Creating our APIkey Credentials
# see: https://firebase.google.com/docs/admin/setup#python_1

# # Add a new document
# db = firestore.Client()
#doc_ref = db.collection(u'users').document(u'alovelace')
#doc_ref.set({
  #  u'first': u'Ada',
  #  u'last': u'Lovelace',
  #  u'born': 1815
#})

# # Then query for documents
# users_ref = db.collection(u'users')

# for doc in users_ref.stream():
#     print(u'{} => {}'.format(doc.id, doc.to_dict()))


#garage = 'schrank','church','admin',etc

def updateDatabase(garage):
    db = firestore.Client()
    collection = db.collection(u'Garages').document(garage)
    collection.set({
        u'currentCars': Increment(1)
    }, merge=True)
    count = collection.get().to_dict()['currentCars']
    print(count)
    return count


updateDatabase('Admin')
