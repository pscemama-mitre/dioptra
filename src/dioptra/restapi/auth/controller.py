# This Software (Dioptra) is being made available as a public service by the
# National Institute of Standards and Technology (NIST), an Agency of the United
# States Department of Commerce. This software was developed in part by employees of
# NIST and in part by NIST contractors. Copyright in portions of this software that
# were developed by NIST contractors has been licensed or assigned to NIST. Pursuant
# to Title 17 United States Code Section 105, works of NIST employees are not
# subject to copyright protection in the United States. However, NIST may hold
# international copyright in software created by its employees and domestic
# copyright (or licensing rights) in portions of software that were assigned or
# licensed to NIST. To the extent that NIST holds copyright in this software, it is
# being made available under the Creative Commons Attribution 4.0 International
# license (CC BY 4.0). The disclaimers of the CC BY 4.0 license apply to all parts
# of the software developed or licensed by NIST.
#
# ACCESS THE FULL CC BY 4.0 LICENSE HERE:
# https://creativecommons.org/licenses/by/4.0/legalcode
"""The module defining the auth endpoints."""
from __future__ import annotations

import uuid

import structlog
from flask import request
from flask.wrappers import Response
from flask_accepts import accepts
from flask_login import login_required
from flask_restx import Namespace, Resource
from injector import inject
from structlog.stdlib import BoundLogger

from dioptra.restapi.utils import as_api_parser

from .schema import LoginSchema
from .service import AuthService

LOGGER: BoundLogger = structlog.stdlib.get_logger()

api: Namespace = Namespace(
    "Authentication",
    description="Authentication endpoint",
)


@api.route("/login")
class LoginResource(Resource):

    @inject
    def __init__(self, *args, auth_service: AuthService, **kwargs) -> None:
        self._auth_service = auth_service
        super().__init__(*args, **kwargs)

    @api.expect(as_api_parser(api, LoginSchema))
    @accepts(schema=LoginSchema, api=auth_api)
    def post(self) -> Response:
        """Attempts to login a user with the provide credentials."""
        log: BoundLogger = LOGGER.new(
            request_id=str(uuid.uuid4()), resource="auth", request_type="POST"
        )
        return self._auth_service.login(data=request.parsed_obj, log=log)
        # return self._auth_service.login(login_data=request.parsed_obj, log=log)

@api.route("/logout")
class LogoutResource(Resource):

    @inject
    def __init__(self, *args, auth_service: AuthService, **kwargs) -> None:
        self._auth_service = auth_service
        super().__init__(*args, **kwargs)

    @login_required
    def post(self) -> Response:
        """Attempts to logout the current user."""
        log: BoundLogger = LOGGER.new(
            request_id=str(uuid.uuid4()), resource="auth", request_type="POST"
        )
        return self._auth_service.logout(request=request, log=log)
