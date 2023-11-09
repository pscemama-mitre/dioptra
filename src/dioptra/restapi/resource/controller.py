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
"""The module defining the group endpoints."""
from __future__ import annotations

import uuid
from typing import List, Optional

import structlog
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from injector import inject
from structlog.stdlib import BoundLogger

from dioptra.restapi.utils import slugify

from .errors import GroupDoesNotExistError
from .model import Group
from .schema import GroupSchema
from .service import GroupService

LOGGER: BoundLogger = structlog.stdlib.get_logger()

api: Namespace = Namespace(
    "DioptraResource",
    description="Dioptra Resource submission and management operations",
)

@api.route("/")
class DioptraResourceResource(Resource):
    """Shows a list of all Dioptra Resources, and lets you POST to create new Dioptra Resources."""

    @inject
    def __init__(
        self,
        *args,
        dioptra_resource_service: DioptraResourceService,
        **kwargs,
    ) -> None:
        self._dioptra_resource_service = dioptra_resource_service
        super().__init__(*args, **kwargs)

    @responds(schema=DioptraResourceSchema(many=True), api=api)
    def get(self) -> List[DioptraResource]:
        """Gets a list of all Dioptra Resources."""
        log: BoundLogger = LOGGER.new(
            request_id=str(uuid.uuid4()), resource="dioptra_resource", request_type="GET"
        )  # noqa: F841
        log.info("Request received")
        return self._dioptra_resource_service.get_all(log=log)

    @accepts(DioptraResourceSchema, api=api)
    @responds(schema=DioptraResourceSchema, api=api)
    def post(self) -> DioptraResource:
        """Creates a new Dioptra Resource via a resource submission form with an attached file."""
        log: BoundLogger = LOGGER.new(
            request_id=str(uuid.uuid4()), resource="dioptra_resource", request_type="POST"
        )  # noqa: F841

        log.info("Request received")

        parsed_obj = request.parsed_obj
        owner_id = parsed_obj["owner_id"]
        creator_id = parsed_obj["creator_id"]
        
        return self._dioptra_resource_service.submit(owner_id=owner_id, creator_id=creator_id, log=log)


    @accepts(DioptraResourceSchema, api=api)
    def delete(self) -> bool:
        log: BoundLogger = LOGGER.new(
            request_id=str(uuid.uuid4()), resource="dioptra_resource", request_type="POST"
        )  # noqa: F841

        log.info("Request received")

        parsed_obj = request.parsed_obj  # type: ignore
        resource_id = int(parsed_obj["resource_id"])
        return self._dioptra_resource_service.delete(id=resource_id)



@api.route("/<int:resourceId>")
@api.param("resourceId", "An integer specifying a resource's ID.")
class DioptraResourceIdResource(Resource):
    """Shows a single Dioptra Resource."""

    @inject
    def __init__(
        self,
        *args,
        dioptra_resource_service: DioptraResourceService,
        **kwargs,
    ) -> None:
        self._dioptra_resource_service = dioptra_resource_service
        super().__init__(*args, **kwargs)

    @responds(schema=DioptraResourceSchema, api=api)
    def get(self, resourceId: int) -> DioptraResource:
        """Gets a Dioptra Resource by its unique identifier."""
        log: BoundLogger = LOGGER.new(
            request_id=str(uuid.uuid4()),
            resource="dioptra_resource_id",
            request_type="GET",
        )  # noqa: F841
        log.info("Request received", resource_id=resourceId)
        resource: Optional[DioptraResource] = self._dioptra_resource_service.get_by_id(
            resourceId, log=log
        )

        if resource is None:
            log.error("Dioptra Resource not found", resource_id=resourceId)
            raise DioptraResourceDoesNotExistError

        return resource

