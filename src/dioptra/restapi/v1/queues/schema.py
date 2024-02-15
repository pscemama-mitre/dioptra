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
"""The schemas for serializing/deserializing Queue resources."""
from __future__ import annotations

from marshmallow import Schema, fields

from dioptra.restapi.v1.groups.schema import GroupRefSchema
from dioptra.restapi.v1.schemas import (
    BasePageSchema,
    GroupIdQueryParametersSchema,
    PagingQueryParametersSchema,
    SearchQueryParametersSchema,
)
from dioptra.restapi.v1.tags.schema import TagRefSchema
from dioptra.restapi.v1.users.schema import UserRefSchema

# only use load only and dump only if necessary
# load only means the attribute is only used when creating the object
# dump only means the attribute is only used as a response

# fields.nested is used when mixing in other schemas

# standardize on the descriptions used here, for the most part changing only object
#   names


# used whenever another resource needs the Queue object to hydrate it's response.
# rule for refs: primary key (Id), natural key (name usually), url
class QueueRefSchema(Schema):
    """The reference schema for the data stored in a Queue resource."""

    id = fields.Integer(
        attribute="id",
        metadata=dict(description="ID for the Queue resource."),
    )
    group = fields.Nested(
        GroupRefSchema,
        attribute="group",
        metadata=dict(description="Group that owns the Queue resource."),
    )
    name = fields.String(
        attribute="name",
        metadata=dict(description="Name of the Queue resource."),
    )
    url = fields.Url(
        attribute="url",
        metadata=dict(description="URL for accessing the full Queue resource."),
        relative=True,
    )

# used to handle PUTS
class QueueMutableFieldsSchema(Schema):
    """The fields schema for the mutable data in a Queue resource."""

    name = fields.String(
        attribute="name", metadata=dict(description="Name of the Queue resource.")
    )
    description = fields.String(
        attribute="description",
        metadata=dict(description="Description of the Queue resource."),
    )

# for the moment wil never be passed to the controller
class QueueBaseSchema(Schema):
    """The base schema for the data stored in a Queue resource."""

    id = fields.Integer(  # id is the same as resource id
        attribute="id",
        metadata=dict(description="ID for the Queue resource."),
        dump_only=True,
    )
    snapshotId = fields.Integer(  # only exists on snapshot types
        attribute="snapshot_id",
        metadata=dict(description="ID for the underlying resource snapshot."),
        dump_only=True,
    )
    groupId = fields.Integer(  # is only used during creation of a Queue, thus load_only
        attribute="group_id",
        metadata=dict(description="ID of the Group that will own the Queue resource."),
        load_only=True,
    )
    group = (
        fields.Nested(  # is only returned as a response, after creation using groupID
            GroupRefSchema,
            attribute="group",
            metadata=dict(description="Group that owns the Queue resource."),
            dump_only=True,
        )
    )
    user = (
        fields.Nested(  # hydrated, user is set based on the logged in user on creation
            UserRefSchema,
            attribute="user",
            metadata=dict(description="User that created the Queue resource."),
            dump_only=True,
        )
    )
    createdOn = fields.DateTime(  # inferred from the underlying resource
        attribute="created_on",
        metadata=dict(description="Timestamp when the Queue resource was created."),
        dump_only=True,
    )
    lastModifiedOn = fields.DateTime(  # inferred from underlying snapshot
        attribute="last_modified_on",
        metadata=dict(
            description="Timestamp when the Queue resource was last modified."
        ),
        dump_only=True,
    )
    tags = fields.Nested(  # hydrated field
        TagRefSchema,
        attribute="tags",
        metadata=dict(description="Tags associated with the Queue resource."),
        many=True,
        dump_only=True,
    )
# full schema to be used with both accepts and responds, for GET and POST
# The order of inheritance matters, where fields from the first schema
# appear at the bottom.
class QueueSchema(QueueMutableFieldsSchema, QueueBaseSchema):
    """The schema for the data stored in a Queue resource."""

# only change the Resource type in Class name, docstring, and data
class QueuePageSchema(BasePageSchema):
    """The paged schema for the data stored in a Queue resource."""

    data = fields.Nested(
        QueueSchema,
        many=True,
        metadata=dict(description="List of Queue resources in the current page."),
    )


class QueueGetQueryParameters(
    PagingQueryParametersSchema,
    GroupIdQueryParametersSchema,
    SearchQueryParametersSchema,
):
    """The query parameters for the GET method of the /queues endpoint."""
