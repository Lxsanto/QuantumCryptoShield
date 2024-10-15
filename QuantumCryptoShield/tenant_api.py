# tenant_api.py

import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
import uuid
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configurazione del database
mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
print(f"Utilizzando MONGO_URI: {mongo_uri}")
client = MongoClient(mongo_uri)
db = client['shieldq_database']

@app.route('/create_tenant', methods=['POST'])
def create_tenant():
    data = request.get_json()
    company_name = data.get('company_name')
    plan = data.get('plan')

    if not company_name or not plan:
        return jsonify({'error': 'company_name e plan sono campi obbligatori'}), 400

    tenant_id = str(uuid.uuid4())
    api_key = str(uuid.uuid4())

    tenant_data = {
        'tenant_id': tenant_id,
        'company_name': company_name,
        'plan': plan,
        'api_key': api_key
    }
    db.tenants.insert_one(tenant_data)

    return jsonify({
        'tenant_id': tenant_id,
        'api_key': api_key
    }), 201

if __name__ == '__main__':
    app.run(port=5004)
