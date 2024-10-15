# services/zkp_service.py

import hashlib

class ZeroKnowledgeProofService:
    def generate_proof(self, secret):
        # Simula la generazione della prova
        commitment = hashlib.sha256(secret.encode('utf-8')).hexdigest()
        return {'proof': commitment}

    def verify_proof(self, proof, secret):
        expected_commitment = hashlib.sha256(secret.encode('utf-8')).hexdigest()
        return proof == expected_commitment
