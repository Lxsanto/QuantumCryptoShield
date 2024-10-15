# key_management_api.py

import os
import sys
from flask import Flask, request, jsonify
from pymongo import MongoClient
from functools import wraps
from flask_cors import CORS

# Aggiungi il percorso corrente al PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.auth_service import authenticate
from services.key_rotation_service import KeyRotationService
from services.encryption_service import EncryptionService

app = Flask(__name__)
CORS(app)

# Configurazione del database
mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(mongo_uri)
db = client['shieldq_database']

key_rotation_service = KeyRotationService(db)
encryption_service = EncryptionService(db)

@app.route('/<tenant_id>/keygen', methods=['POST'])
@authenticate
def keygen(tenant_id):
    # Genera le chiavi utilizzando EncryptionService
    encryption_service.generate_keys(tenant_id)
    return jsonify({'message': 'Chiavi generate con successo'}), 200

if __name__ == '__main__':
    app.run(port=5003)
