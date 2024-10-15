# encryption_api.py

import os
import sys
from flask import Flask, request, jsonify
from pymongo import MongoClient
from functools import wraps
from flask_cors import CORS

# Aggiungi il percorso corrente al PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.auth_service import authenticate
from services.encryption_service import EncryptionService

app = Flask(__name__)
CORS(app)

# Configurazione del database
mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(mongo_uri)
db = client['shieldq_database']

encryption_service = EncryptionService(db)

@app.route('/<tenant_id>/encrypt', methods=['POST'])
@authenticate
def encrypt(tenant_id):
    data = request.get_json()
    message = data.get('message')

    if not message:
        return jsonify({'error': 'Message is required'}), 400

    encrypted_message = encryption_service.encrypt(tenant_id, message)

    if encrypted_message is None:
        return jsonify({'error': 'Encryption failed'}), 500

    return jsonify({'encrypted_message': encrypted_message}), 200

@app.route('/<tenant_id>/decrypt', methods=['POST'])
@authenticate
def decrypt(tenant_id):
    data = request.get_json()
    encrypted_message = data.get('encrypted_message')

    if not encrypted_message:
        return jsonify({'error': 'Encrypted message is required'}), 400

    message = encryption_service.decrypt(tenant_id, encrypted_message)

    if message is None:
        return jsonify({'error': 'Decryption failed'}), 500

    return jsonify({'decrypted_message': message}), 200

if __name__ == '__main__':
    app.run(port=5001)
