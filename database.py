from google.cloud import firestore
from google.auth import credentials
from google.cloud.firestore import Increment
import firebase_admin
import asyncio

class Database:
    def __init__(self, garage):
        default_app = firebase_admin.initialize_app()
        self.db = firestore.AsyncClient()
        self.garage=garage

#garage = 'schrank','church','admin',etc
    
    async def DecDatabase(self) -> int:
        collection = self.db.collection(u'Garages').document(self.garage)
        await collection.set({
            u'currentCars': Increment(-1)
        }, merge=True)
        #print(count)
        return 

    async def IncDatabase(self) -> int:
        collection = self.db.collection(u'Garages').document(self.garage)
        await collection.set({
            u'currentCars': Increment(1)
        }, merge=True)
        #print(count)
        return 


    async def getCurrentCount(self) -> int:
        collection = await self.db.collection(u'Garages').document(self.garage).get()
        return collection.to_dict()['currentCars']
