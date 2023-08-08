# a simple page that says hello
import flask
import flask_login

from flask import Blueprint

bp = Blueprint('api', __name__, url_prefix='/')

@bp.route('/hello', methods=['GET', 'PUT', 'POST'])
def hello():
    return 'Hello, World!'

@bp.route('/test', methods=['GET', 'PUT', 'POST'])
@flask_login.login_required
def test():
    return flask.current_app.config.get('SECRET_KEY')

@bp.route('/world', methods=['GET', 'PUT', 'POST'])
@flask_login.login_required
def world():
    return flask.jsonify(flask_login.current_user.to_json())

@bp.route('/foo', methods=['GET', 'PUT', 'POST'])
@flask_login.login_required
def foo():
    if flask.request.method == 'POST':
        if flask.request.content_type != 'application/json':
            return {'message': 'unknown input'}, 400
        return flask.request.json
    return 'bar'