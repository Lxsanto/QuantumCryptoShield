import os
from functools import wraps
from flask import request, jsonify
from pymongo import MongoClient

# Configurazione del database
mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(mongo_uri)
db = client['shieldq_database']

def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization', None)
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Missing or invalid Authorization Header"}), 401
        api_key = auth_header.split(' ')[1]
        tenant_id = kwargs.get('tenant_id')

        tenant = db.tenants.find_one({'tenant_id': tenant_id, 'api_key': api_key})

        if not tenant:
            return jsonify({'error': 'Invalid API Key'}), 401

        return f(*args, **kwargs)
    return decorated_function
