import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from services.quantum_key_service import QuantumKeyService

class EncryptionService:
    def __init__(self, db):
        self.db = db
        self.qrng_service = QuantumKeyService()

    def generate_keys(self, tenant_id):
        quantum_key = self.qrng_service.generate_qrng_key(length=32)
        if not quantum_key:
            quantum_key = os.urandom(32)

        self.db.keys.update_one(
            {'tenant_id': tenant_id},
            {'$set': {'symmetric_key': quantum_key.hex()}},
            upsert=True
        )

    def encrypt(self, tenant_id, message):
        key_data = self.db.keys.find_one({'tenant_id': tenant_id})
        if not key_data or not key_data.get('symmetric_key'):
            return None

        key = bytes.fromhex(key_data['symmetric_key'])
        iv = os.urandom(16)  

        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(message.encode('utf-8')) + padder.finalize()

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        return (iv + ciphertext).hex()

    def decrypt(self, tenant_id, encrypted_message):
        key_data = self.db.keys.find_one({'tenant_id': tenant_id})
        if not key_data or not key_data.get('symmetric_key'):
            return None

        key = bytes.fromhex(key_data['symmetric_key'])
        encrypted_data = bytes.fromhex(encrypted_message)

        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:]

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

        return plaintext.decode('utf-8')
