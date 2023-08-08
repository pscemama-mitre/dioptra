import logging
import os

from flask import Flask
from flask_login import LoginManager


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY="dev")

    logging.basicConfig(level=logging.DEBUG)
    # logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.DEBUG)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # set-up login
    login_manager = LoginManager()
    from . import user

    login_manager.request_loader(user.load_user_from_request)
    login_manager.init_app(app)

    from . import auth

    app.register_blueprint(auth.bp)

    from . import api

    app.register_blueprint(api.bp)

    # flask-wtf by default tries to set/check a csrf token on everything... we
    # don't want to mess with that for this experimentation, so turn off csrf if requested
    if app.config.get("DISABLE_CSRF") == 1:
        logging.info("disabling CSRF")
        app.config["WTF_CSRF_ENABLED"] = False

    if app.config.get("ENABLE_RESTX") == 1:
        logging.info("registering restx")
        from . import form

        form.register_restx(app)

    return app
