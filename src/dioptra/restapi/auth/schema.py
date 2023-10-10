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
"""The schemas for serializing/deserializing the auth endpoint objects.

.. |User| replace:: :py:class:`~.model.User`
.. |UserRegistrationForm| replace:: :py:class:`~.model.UserRegistrationForm`
"""
from __future__ import annotations

from marshmallow import Schema, fields


class LoginRequestSchema(Schema):
    username = fields.String(
        attribute="username",
        metadata=dict(description="The username for logging into the user account."),
    )
    password = fields.String(
        attribute="password",
        metadata=dict(description="The password used for authenticating the user account."),
    )

class LogoutRequestSchema(Schema):
    everywhere = fields.Bool(
        attribute="everywhere",
        metadata=dict(description="If True, log out from all devices."),
        load_default=lambda: False,
    )

class LoginResponseSchema(Schema):
    status = fields.Int(
        attribute="status",
        metadata=dict(description="The repsonse code for a successful login request."),
    )
    message = fields.String(
        attribute="message",
        metadata=dict(description="A successful login message."),
    )

class LogoutResponseSchema(Schema):
    status = fields.Int(
        attribute="status",
        metadata=dict(description="The repsonse code for a successful logout request."),
    )
    message = fields.String(
        attribute="message",
        metadata=dict(description="A successful logout message."),
    )
