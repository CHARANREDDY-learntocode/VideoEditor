from functools import wraps
from flask import request, jsonify

# Static API tokens for simplicity (store securely in production)
VALID_TOKENS = {"example-token-123", "example-token-456"}


def authenticate():
    print("hii")
    token = request.headers.get('Authorization')

    if not token or not token.startswith("Bearer "):
        return

    token = token.split(" ")[1]
    if token not in VALID_TOKENS:
        raise Exception("Not authorized")
