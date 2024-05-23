import secrets
import hashlib

def generate_random_hash(length: int = 16) -> str:
    random_bytes = secrets.token_bytes(length)
    return hashlib.sha256(random_bytes).hexdigest()
