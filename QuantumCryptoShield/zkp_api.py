# zkp_api.py

import os
import sys
from flask import Flask, request, jsonify
from pymongo import MongoClient
from functools import wraps
from flask_cors import CORS

# Aggiungi il percorso corrente al PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.auth_service import authenticate
from services.zkp_service import ZeroKnowledgeProofService

app = Flask(__name__)
CORS(app)

# Configurazione del database
mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(mongo_uri)
db = client['shieldq_database']

zkp_service = ZeroKnowledgeProofService()

@app.route('/<tenant_id>/zkp/generate', methods=['POST'])
@authenticate
def generate_proof(tenant_id):
    data = request.get_json()
    secret = data.get('secret')

    if not secret:
        return jsonify({'error': 'Secret is required'}), 400

    proof = zkp_service.generate_proof(secret)
    return jsonify(proof), 200

@app.route('/<tenant_id>/zkp/verify', methods=['POST'])
@authenticate
def verify_proof(tenant_id):
    data = request.get_json()
    proof = data.get('proof')
    secret = data.get('secret')

    if not proof or not secret:
        return jsonify({'error': 'Proof and secret are required'}), 400

    is_valid = zkp_service.verify_proof(proof, secret)
    return jsonify({'is_valid': is_valid}), 200

if __name__ == '__main__':
    app.run(port=5002)
