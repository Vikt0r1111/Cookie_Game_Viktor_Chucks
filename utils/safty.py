import hashlib

def data_chacher(data):
    data_encoded = data.encode("utf-8")
    hash_object = hashlib.sha256(data_encoded)
    hesh_hex = hash_object.hexdigest()
    return hesh_hex

