# services/tenant_service.py

import os
from pymongo import MongoClient, errors

class TenantService:
    def __init__(self):
        mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
        try:
            self.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            self.db = self.client['shieldq_database']
        except errors.ServerSelectionTimeoutError as err:
            raise Exception("Database connection failed") from err

    def validate_api_key(self, api_key):
        tenant = self.db.tenants.find_one({"api_key": api_key})
        return tenant is not None
