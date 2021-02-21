from google.cloud import firestore
from google.auth import credentials
from google.cloud.firestore import Increment
import firebase_admin

# cred = credentials.Certificate("path/to/serviceAccountKey.json")
# firebase_admin.initialize_app(cred)


class Database:
    def __init__(self):
        default_app = firebase_admin.initialize_app()
        self.db = firestore.Client()


# Network comms w/ DB
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore

# Creating our APIkey Credentials
# see: https://firebase.google.com/docs/admin/setup#python_1

# # Add a new document
# db = firestore.Client()
#doc_ref = db.collection(u'users').document(u'alovelace')
# doc_ref.set({
    #  u'first': u'Ada',
    #  u'last': u'Lovelace',
    #  u'born': 1815
# })

# # Then query for documents
# users_ref = db.collection(u'users')

# for doc in users_ref.stream():
#     print(u'{} => {}'.format(doc.id, doc.to_dict()))


#garage = 'schrank','church','admin',etc


    async def DecDatabase(self, garage) -> int:
        collection = await self.db.collection(u'Garages').document(garage)
        await collection.set({
            u'currentCars': Increment(-1)
        }, merge=True)
        count = await collection.get().to_dict()['currentCars']
        return count

    async def IncDatabase(self, garage) -> int:
        collection = await self.db.collection(u'Garages').document(garage)
        await collection.set({
            u'currentCars': Increment(1)
        }, merge=True)
        count = await collection.get().to_dict()['currentCars']
        return count

    async def getCurrentCount(self, garage) -> int:
        collection = await self.db.collection(u'Garages').document(garage)
        return collection.get().to_dict()['currentCars']
