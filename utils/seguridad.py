import hashlib
import os

def crear_password_hash(password):
    """Genera un hash seguro para la contraseña usando PBKDF2."""
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt + key 

def verificar_password(password, stored_password):
    """Verifica si la contraseña coincide con el hash almacenado."""
    salt = stored_password[:32]
    key = stored_password[32:]
    new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return key == new_key

def hash_to_string(hash_bytes):
    """Convierte los bytes del hash a string hexadecimal para almacenamiento."""
    return hash_bytes.hex()

def string_to_hash(hash_string):
    """Convierte el string hexadecimal de vuelta a bytes."""
    return bytes.fromhex(hash_string)
