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
"""The server-side functions that perform auth endpoint operations."""
from __future__ import annotations

import structlog
from typing import Any
from flask import Request, Response, jsonify
from flask_login import current_user, login_user, logout_user
from injector import inject
from sqlalchemy import select
from structlog.stdlib import BoundLogger

from dioptra.restapi.user.service import UserService
from dioptra.restapi.user.errors import UserDoesNotExistError

from .errors import LoginError, LogoutError
from .model import LoginData

LOGGER: BoundLogger = structlog.stdlib.get_logger()


class AuthService(object):

    @inject
    def __init__(
        self, 
        user_service: UserService, # If controller not found thenn injection failed and need to update dependencies to handle UserService
    ) -> None:
        self._user_service = user_service

    def login(
        self, 
        login_data: LoginData,
        **kwargs,
    ) -> Response:
        log: BoundLogger = kwargs.get("log", LOGGER.new())
        username = login_data.get("username", "guest")
        password = login_data.get("password", "")
        user = self._user_service.authenticate_user(name=username, password=password)

        if not user:
            log.info("The requested user does not exist.", username=username)
            raise LoginError

        login_user(user)

        log.info(
            "Login successful",
            user_id=user.user_id,
        )

        return {"status": 200, "message": "Login successful."}

    def logout(
        self, 
        request: Request,
        **kwargs,
    ) -> Response:
        log: BoundLogger = kwargs.get("log", LOGGER.new())
        logout_user()

        '''
        When there is no user logged in current_user returns
        AnonymousUserMixin object that has .is_authenticated
        set to False.

        See:
        - https://flask-login.readthedocs.io/en/latest/#anonymous-users
        - https://flask-login.readthedocs.io/en/latest/#flask_login.AnonymousUserMixin
        '''
        if current_user.is_authenticated:
            log.info("The current user was not logged out.", user_id=current_user.user_id)
            raise LogoutError

        log.info(
            "Logout Successful"
        )

        return {"status": 200, "message": "Logout successful."}
