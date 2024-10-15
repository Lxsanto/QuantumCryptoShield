# services/key_rotation_service.py

class KeyRotationService:
    def __init__(self, db):
        self.db = db

    def rotate_key(self, tenant_id):
        # Richiama la generazione delle chiavi
        from services.encryption_service import EncryptionService
        encryption_service = EncryptionService(self.db)
        encryption_service.generate_keys(tenant_id)
        return True
