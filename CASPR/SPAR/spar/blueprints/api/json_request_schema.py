upload_signing_key_request = {
    "public_key": {"type": "string", "required": True},
    "fingerprint": {"type": "string", "required": True},
    "email": {"type": "string", "required": True}
}


get_signing_key_request = {
    "keyid": {"type": "string", "required": True},
}

remove_signing_key_request = {
    "fingerprint": {"type": "string", "required": True},
}