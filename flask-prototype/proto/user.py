from datetime import datetime

import jwt
from jose import jwk
from flask import request
from werkzeug.security import check_password_hash, generate_password_hash

from .auth import pub_key


class User:
    def __init__(self, id: int, name: str, password: str):
        self.id = id
        self.name = name
        self.password = generate_password_hash(password)

    def to_json(self):
        return {"name": self.name}

    def is_authenticated(self) -> bool:
        return True

    def is_active(self) -> bool:
        return True

    def is_anonymous(self) -> bool:
        return False

    def get_id(self) -> str:
        return str(self.id)


# very simplistic user store
users: dict = {
    "1": User(1, "user", "password"),
    "2": User(2, "joe", "hashed"),
}


def authenticate_user(name: str, password: str) -> None | User:
    for u in users.values():
        if u.name == name:
            if check_password_hash(u.password, password):
                return u
            break
    return None


def load_user(id: str) -> None | User:
    return users.get(id)


def load_user_from_request(request: request) -> None | User:
    encoded = None
    if "x-access-token" in request.headers:
        encoded = request.headers["x-access-token"]
    if not encoded:
        return None
    token = jwt.decode(encoded, pub_key, algorithms="RS256")
    return load_user(token["id"])
