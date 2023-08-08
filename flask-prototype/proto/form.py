import flask

from flask import Flask
import flask_accepts
import flask_restx
import flask_restx.fields as fields
import flask_restx.reqparse as reqparse
import flask_wtf
import marshmallow
import wtforms.fields
   
def register_restx(app: Flask):
    restx = flask_restx.Api(app, prefix="/restx")

    hello_get_response_model = restx.model("resp_model", {
        "hello": fields.String,
        "foo": fields.Integer
    })

    # The marshmallow version of the above schema (via an API which does not
    # require creating a class, as dioptra does).
    hello_get_response_model_marsh = marshmallow.Schema.from_dict({
        "hello": marshmallow.fields.String(dump_default="world"),
        "foo": marshmallow.fields.Integer()
    })

    hello_post_request_model = restx.model("req_model", {
        "A": fields.Boolean,
        "B": fields.Float
    })

    # The marshmallow version of the above schema
    hello_post_request_model_marsh = marshmallow.Schema.from_dict({
        "A": marshmallow.fields.Boolean(),
        "B": marshmallow.fields.Float(load_default=3.14)
    })

    hello_post_request_model_reqparse = reqparse.RequestParser()
    hello_post_request_model_reqparse.add_argument(
        "A", type=bool, help="Argument A"
    )
    hello_post_request_model_reqparse.add_argument(
        "B", type=float, help="Argument B"
    )

    @restx.route('/hello')
    class HelloWorld(flask_restx.Resource):
        # @restx.response only adds documentation.  One can use
        # @restx.marshal_with to obtain automatic dict creation from a
        # non-dict (with validation).  I think if you use @marshal_with, you
        # don't also need @response.
        #
        # If response marshalling fails, you just get an internal server crash
        # and 500 response.  True both with restx and flask-accepts.
        #
        # When using flask-accepts with marshmallow, the actual restx
        # annotations (from which swagger docs are derived) are translations
        # from marshmallow field types, to restx field types.  Validation
        # happens via the marshmallow schema though.

        # @restx.response(200, "Success", hello_get_response_model)
        # @restx.marshal_with(hello_get_response_model)
        @flask_accepts.responds("resp_model", schema=hello_get_response_model_marsh, api=restx)
        def get(self):
            return {
                # Commenting out the below property causes the marshmallow
                # dump_default to kick in, for testing.
                # 'hello': 'world',
                "foo": 1
            }

        # The below does not work for validation: RequestParsers must be
        # invoked manually.  The automatic payload validation only works with
        # models.  However, we do get swagger documentation.
        # @restx.expect(hello_post_request_model_reqparse, validate=True)
        #
        # When using a model, we get both documentation and automatic request
        # payload validation.  The model goes into a separate model schema
        # section of the swagger documentation.
        # @restx.expect(hello_post_request_model, validate=True)
        @flask_accepts.accepts("req_model", schema=hello_post_request_model_marsh, api=restx)
        def post(self):
            app.logger.info("Raw request payload: %s", flask.request.get_data(as_text=True))
            app.logger.info("JSON payload: %s", str(flask.request.json))
            app.logger.info(
                "Marshmallow load result: %s", str(flask.request.parsed_obj)
            )

            # How we could do manual validation with RequestParser:
            # args = hello_post_request_model_reqparse.parse_args(strict=True)
            # app.logger.error("Reqparse results: %s", str(args))

            return "", 200

    # To see all the restx documentation junk it attaches to these methods...
    print("Get restx annotations:", HelloWorld.get.__apidoc__)
    print("Post restx annotations:", HelloWorld.post.__apidoc__)

    class MyForm(flask_wtf.FlaskForm):
        name = wtforms.fields.StringField()
        age = wtforms.fields.IntegerField()

    @restx.route("/form")
    class FormTest(flask_restx.Resource):
        def post(self):
            form = MyForm()
            app.logger.info("flask_wtf form: %s", str(form.data))

            if not form.validate_on_submit():
                flask.abort(400)

            return "", 200
