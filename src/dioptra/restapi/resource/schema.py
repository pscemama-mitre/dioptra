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
"""The schemas for serializing/deserializing the DioptraResource endpoint objects.

.. |Job| replace:: :py:class:`~.model.Job`
"""
from __future__ import annotations

from typing import Any, Dict

from marshmallow import Schema, fields, post_load

from .model import DioptraResource


class DioptraResourceSchema(Schema):
    """The schema for the data stored in a |DioptraResource| object.

    Attributes:
        id: The unique identifier of the resource.
        creator_id: The id for the user that created the resource.
        owner_id: The id for the group that owns the resource.
        created_on: The time at which the resource was created.
        last_modified_on: The time at which the resource was last modified.
        is_deleted: Whether the resource has been deleted.
    """

    __model__ = DioptraResource

    id = fields.Integer(
        attribute="id", metadata=dict(description="The unique identifier of the resource.")
    )
    creator_id = fields.Integer(
        attribute="creator_id",
        metadata=dict(
            description="An integer identifying the user that created the resource."
        ),
    )
    owner_id = fields.Integer(
        attribute="owner_id",
        metadata=dict(description="An integer identifying the group that owns the resource."),
    )
    created_on = fields.DateTime(
        attribute="created_on",
        metadata=dict(description="The date and time the resource was created."),
    )
    last_modified_on = fields.DateTime(
        attribute="last_modified_on",
        metadata=dict(description="The date and time the resource was last modified."),
    )
    is_deleted = fields.Boolean(
        attribute="is_deleted",
        metadata=dict(description="Whether the resource has been deleted."),
    )

    @post_load
    def deserialize_object(self, data: Dict[str, Any], many: bool, **kwargs) -> DioptraResource:
        """Creates a |DioptraResource| object from the validated data."""
        return self.__model__(**data)