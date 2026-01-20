import hashlib
import string
import secrets
import base64
import json
from dotenv import load_dotenv
from itsdangerous import URLSafeTimedSerializer, BadSignature

def data_chacher(data):
    data_encoded = data.encode("utf-8")
    hash_object = hashlib.sha256(data_encoded)
    hesh_hex = hash_object.hexdigest()
    return hesh_hex

def decode_base64(first_part):
    load_dotenv()
    
    s = URLSafeTimedSerializer()

def session_cutter(full_session):
    parts = full_session.split(".")
    first_part = parts[0]
    return first_part
    

