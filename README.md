#QuantumCryptoShield is a Python-based framework focused on secure cryptographic operations and key management in a quantum-safe environment. It includes modular APIs and services that provide robust encryption, tenant and key management, zero-knowledge proof (ZKP) verification, and advanced quantum key rotation capabilities. Designed for scalable and secure deployment, QuantumCryptoShield ensures data integrity and confidentiality against current and post-quantum threats.

#Main Features:

- Secure tenant and key management services
- Quantum-safe encryption and decryption
- Zero-Knowledge Proof (ZKP) verification API
- Quantum key rotation and lifecycle management
- Extensible APIs for seamless integration

# Application Setup and Usage Instructions

## Prerequisites
- MongoDB running on `localhost:27017`
- Python installed on your system

## 1. Start MongoDB
Ensure the MongoDB service is running on `localhost:27017`.

## 2. Run the APIs
In separate terminals, run each API:

### Tenant API:
```bash
python tenant_api.py
```

### Key Management API:
```bash
python key_management_api.py
```

### Encryption API:
```bash
python encryption_api.py
```

### ZKP API:
```bash
python zkp_api.py
```

## 3. Create a Tenant
In a new terminal, execute:

```bash
curl -X POST \
  http://localhost:5004/create_tenant \
  -H 'Content-Type: application/json' \
  -d '{
    "company_name": "Your Company",
    "plan": "Premium"
  }'
```

Note the returned `tenant_id` and `api_key`.

## 4. Configure the Dashboard
In the `dashboard/main.js` file, replace:

```javascript
const tenantId = 'YOUR_TENANT_ID'; // Insert the obtained tenant_id
const apiKey = 'YOUR_API_KEY'; // Insert the obtained api_key
```

## 5. Start the Dashboard
Navigate to the `dashboard/` directory and run:

```bash
python -m http.server 8080
```

Access the dashboard via `http://localhost:8080` in your browser.

## 6. Use the Application
- **Generate Keys:** Click the "Generate Keys" button on the dashboard.
- **Encrypt a Message:** Enter a message in the "Encrypt Message" field and click "Encrypt Message".
- **Decrypt a Message:** Enter the encrypted message in the "Decrypt Message" field and click "Decrypt Message".

## Troubleshooting
If you encounter any issues, please check the following:
- Ensure all API services are running
- Verify the MongoDB connection
- Check the browser console for any JavaScript errors

For further assistance, please contact our support team.
