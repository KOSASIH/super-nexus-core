import hashlib
import hmac
import os

class CryptoUtils:
    @staticmethod
    def hash_sha256(data: bytes) -> str:
        """Generate SHA-256 hash of the input data."""
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def generate_salt(length: int = 16) -> bytes:
        """Generate a random salt."""
        return os.urandom(length)

    @staticmethod
    def hmac_sha256(key: bytes, message: bytes) -> str:
        """Generate HMAC using SHA-256."""
        return hmac.new(key, message, hashlib.sha256).hexdigest()

# Example usage
if __name__ == "__main__":
    data = b"Hello, World!"
    salt = CryptoUtils.generate_salt()
    hashed = CryptoUtils.hash_sha256(data)
    hmac_result = CryptoUtils.hmac_sha256(salt, data)

    print(f"Hash: {hashed}")
    print(f"Salt: {salt.hex()}")
    print(f"HMAC: {hmac_result}")
