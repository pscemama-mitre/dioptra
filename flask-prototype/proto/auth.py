import json
from datetime import datetime, timedelta, timezone

import flask
import flask_login
import jwt
from flask import Blueprint, request

from . import user as user_module

bp = Blueprint("auth", __name__, url_prefix="/auth")

with open("proto/vault/jwt_key", "r") as privatefile:
    priv_key = privatefile.read()
    privatefile.close()

with open("proto/vault/jwt_key.pub", "r") as publicfile:
    pub_key = publicfile.read()
    publicfile.close()


@bp.route("/login", methods=["POST"])
def login():
    info = json.loads(request.data)
    username = info.get("username", "guest")
    password = info.get("password", "")
    user = user_module.authenticate_user(name=username, password=password)
    if user:
        flask_login.login_user(user)

        token = {
            "id": f"{user.id}",
            "username": user.name,
            "iat": datetime.now(tz=timezone.utc),
            "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=30),
        }
        
        # encrypting with private key for signing
        encoded = jwt.encode(token, priv_key, algorithm="RS256")
        return flask.jsonify(encoded)

    else:
        return (
            flask.jsonify({"status": 401, "reason": "Username or Password Error"}),
            401,
        )


@bp.route("/logout", methods=["POST"])
def logout():
    flask_login.logout_user()
    return flask.jsonify(**{"result": 200, "data": {"message": "logout success"}})
