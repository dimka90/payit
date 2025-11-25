import base64
import json

def base64_url_decode(token)-> bytes:
    padding = '='* (-len(token)% 4)

    return base64.urlsafe_b64decode(token + padding)


def decode_jwt(token) -> dict:
    header_base64, payload_base64, signature = token.split('.')
    header = json.loads(base64_url_decode(header_base64))
    payload = json.loads(base64_url_decode(payload_base64))
    return {"header": header, "payload": payload, "sig": signature}

result = decode_jwt("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0IiwiZW1haWwiOiJzYW11ZWxAZXhhbXBsZS5jb20iLCJ1c2VyX2lkIjoiNCIsImV4cCI6MTc2NDA3MzIxMn0.UriN78kxJJ2jpVMtakVZno5yzRpBFLm6gQ33v_PZT4E")
print(result)