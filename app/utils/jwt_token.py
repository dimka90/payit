import base64
import json
from typing import Dict

def decode_jwt_str(input_str)-> bytes:
    padding = '=' * (-len(input_str) % 4)
    return base64.urlsafe_b64decode(input_str + padding)

def decode_jwt_token(token: str) -> Dict:
    header_base64, payload_base64, sig = token.split(".")
    header = json.loads(decode_jwt_str(header_base64))
    payload = json.loads(decode_jwt_str(payload_base64))
    return {
        "header": header,
        "payload": payload,
        "sig": sig
            }


