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
"""The schemas for serializing/deserializing Group resource."""
from __future__ import annotations

from marshmallow import Schema, fields

from dioptra.restapi.v1.schemas import (
    BasePageSchema,
    PagingQueryParametersSchema,
    SearchQueryParametersSchema,
)


class GroupRefSchema(Schema):
    """The reference schema for the data stored in a Group resource."""

    id = fields.Integer(
        attribute="id",
        metadata=dict(description="ID for the Group resource."),
    )
    name = fields.String(
        attribute="name", metadata=dict(description="Name of the Group resource.")
    )
    url = fields.Url(
        attribute="url",
        metadata=dict(description="URL for accessing the full Group resource."),
        relative=True,
    )


class UserGroupBaseSchema(Schema):
    """The fields schema of a Group Member."""

    from dioptra.restapi.v1.users.schema import UserRefSchema

    user = fields.Nested(
        UserRefSchema,
        attribute="user",
        metadata=dict(description="User that is a member of the Group."),
        dump_only=True,
    )
    group = fields.Nested(
        GroupRefSchema,
        attribute="group",
        metadata=dict(description="The Group of which the User is a member."),
        dump_only=True,
    )


class GroupMemberMutableFieldsSchema(Schema):
    """The mutable fields schema of a Group Member."""

    read = fields.Boolean(
        attribute="read",
        metadata=dict(description="Permission for member to read Group."),
    )
    write = fields.Boolean(
        attribute="write",
        metadata=dict(description="Permission for member to modify Group."),
    )
    shareRead = fields.Boolean(
        attribute="share_read",
        metadata=dict(description="Permission for member to share read-only Group."),
    )
    shareWrite = fields.Boolean(
        attribute="share_write",
        metadata=dict(description="Permission for member to share read+write Group."),
    )


class GroupMemberSchema(GroupMemberMutableFieldsSchema, UserGroupBaseSchema):
    """The schema for a Group Member"""


class GroupManagerMutableFieldsSchema(Schema):
    """The mutable fields schema of a Group Manager."""

    owner = fields.Boolean(
        attribute="owner",
        metadata=dict(description="Flag for if the Manager is a Group owner."),
    )
    admin = fields.Boolean(
        attribute="admin",
        metadata=dict(description="Flag for if the Manager is a Group admin."),
    )


class GroupManagerSchema(GroupManagerMutableFieldsSchema, UserGroupBaseSchema):
    """The schema for a Group Manager"""


class GroupMutableFieldsSchema(Schema):
    """The fields schema for the mutable data by GroupMembers in a Group."""

    name = fields.String(
        attribute="name", metadata=dict(description="Name of the Group.")
    )
    members = fields.Nested(
        GroupMemberSchema,
        attribute="members",
        metadata=dict(description="A list of GroupMembers in a Group."),
        many=True,
        dump_only=True,
    )
    managers = fields.Nested(
        GroupManagerSchema,
        attribute="managers",
        metadata=dict(description="A list of Managers in a Group."),
        many=True,
        dump_only=True,
    )


class GroupSchema(GroupMutableFieldsSchema):
    """The schema for the data stored in a Group resource."""

    from dioptra.restapi.v1.users.schema import UserRefSchema

    id = fields.Integer(
        attribute="id",
        metadata=dict(description="ID for the Group resource."),
        dump_only=True,
    )
    user = fields.Nested(
        UserRefSchema,
        attribute="user",
        metadata=dict(description="User that created the Group resource."),
        dump_only=True,
    )
    createdOn = fields.DateTime(
        attribute="created_on",
        metadata=dict(description="Timestamp when the Group resource was created."),
        dump_only=True,
    )
    lastModifiedOn = fields.DateTime(
        attribute="last_modified_on",
        metadata=dict(
            description="Timestamp when the Group resource was last modified."
        ),
        dump_only=True,
    )


class GroupPageSchema(BasePageSchema):
    """The paged schema for the data stored in a Group resource."""

    data = fields.Nested(
        GroupSchema,
        many=True,
        metadata=dict(description="List of Group resources in the current page."),
    )


class GroupGetQueryParameters(
    PagingQueryParametersSchema,
    SearchQueryParametersSchema,
):
    """The query parameters for the GET method of the /groups endpoint."""
