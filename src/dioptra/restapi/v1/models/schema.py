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
"""The schemas for serializing/deserializing Model resources."""
from __future__ import annotations

from marshmallow import fields

from dioptra.restapi.v1.artifacts.schema import ArtifactRefSchema
from dioptra.restapi.v1.schemas import (
    BasePageSchema,
    PagingQueryParametersSchema,
    SearchQueryParametersSchema,
    generate_base_resource_schema,
)

RegisteredModelBaseSchema = generate_base_resource_schema(
    "RegisteredModel", snapshot=False
)


class RegisteredModelSchema(RegisteredModelBaseSchema):  # type: ignore
    """The schema for the data stored in a Registered Model resource."""

    modelId = fields.Integer(
        attribute="model_id",
        metadata=dict(description="The ID of the associated Model resource."),
    )

    versionNumber = fields.Integer(
        attribute="version_number",
        metadata=dict(description="The version number of the Registered Model."),
    )
    artifact = fields.Nested(
        ArtifactRefSchema,
        metadata=dict(description="The artifact registered as the Registered Model."),
    )


class RegisteredModelPageSchema(BasePageSchema):
    """The paged schema for the data stored in a Registered Model resource."""

    data = fields.Nested(
        RegisteredModelSchema,
        many=True,
        metadata=dict(
            description="List of Registered Model resources in the \
                                   current page."
        ),
    )


class RegisteredModelGetQueryParameters(
    PagingQueryParametersSchema,
    SearchQueryParametersSchema,
):
    """The query parameters for the GET method of the
    /models/{id}/versions endpoint."""


ModelBaseSchema = generate_base_resource_schema("Model", snapshot=False)


class ModelSchema(ModelBaseSchema):  # type: ignore
    """The schema for the data stored in a Model resource."""

    name = fields.String(
        attribute="name",
        metadata=dict(description="Name of the Model resource."),
    )
    lastVersion = fields.Nested(
        RegisteredModelSchema,
        attribute="last_version",
        metadata=dict(description="The latest version of the Model resource."),
    )


class ModelPageSchema(BasePageSchema):
    """The paged schema for the data stored in a Model resource."""

    data = fields.Nested(
        ModelSchema,
        many=True,
        metadata=dict(description="List of Model resources in the current page."),
    )


class ModelGetQueryParameters(
    PagingQueryParametersSchema,
    SearchQueryParametersSchema,
):
    """The query parameters for the GET method of the /models endpoint."""
