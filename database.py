from google.cloud import firestore
from google.auth import credentials
from google.cloud.firestore import Increment
import firebase_admin
import threading

# cred = credentials.Certificate("path/to/serviceAccountKey.json")
# firebase_admin.initialize_app(cred)


class Database:
    def __init__(self,garage="Schrank"):
        default_app = firebase_admin.initialize_app()
        self.db = firestore.Client()
        self.garage=garage
        self._lock = threading.Lock()
        self.collection =  self.db.collection(u'Garages').document(garage)
        self.count = self.getCurrentCount()
#garage = 'schrank','church','admin',etc


    def DecDatabase(self) -> int:
        print("Locking Thread DD")
        with self._lock:
            self.collection.set({
                u'currentCars': Increment(-1)
            }, merge=True)
            self.count =  self.collection.get().to_dict()['currentCars']
        print("Unlocking Thread DD")
        return self.count

    def IncDatabase(self) -> int:
        print("Locking Thread ID")
        with self._lock:
            self.collection.set({
                u'currentCars': Increment(1)
            }, merge=True)
            self.count =  self.collection.get().to_dict()['currentCars']
        print("Unlocking Thread ID")
        return self.count

    def getCurrentCount(self) -> int:
        print("Locking Thread GCC")
        with self._lock:
            self.count= self.collection.get().to_dict()['currentCars']
        print("Unlocking Thread GCC")
        return self.count
