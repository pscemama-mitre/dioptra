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
"""The server-side functions that perform job endpoint operations."""
from __future__ import annotations

from datetime import datetime
import structlog
from injector import inject
from dioptra.restapi.app import db
from dioptra.restapi.group_membership.model import GroupMembership
from dioptra.restapi.resource.model import DioptraResource
from sqlalchemy.exc import IntegrityError

from datetime import datetime
from typing import List, Optional

import structlog
from injector import inject
from structlog.stdlib import BoundLogger
from sqlalchemy.exc import IntegrityError

from dioptra.restapi.app import db

from .model import DioptraResource

LOGGER: BoundLogger = structlog.stdlib.get_logger()


class DioptraResourceService(object):
    @staticmethod
    def create(creator_id: int, owner_id: int, **kwargs) -> DioptraResource:
        log: BoundLogger = kwargs.get("log", LOGGER.new())  # noqa: F841
        timestamp = datetime.now()

        return DioptraResource(
            resource_id=DioptraResource.next_id(),
            creator_id=creator_id,
            owner_id=owner_id,
            created_on=timestamp,
            last_modified_on=timestamp,
            is_deleted=False,
        )

    @staticmethod
    def get_all(**kwargs) -> List[DioptraResource]:
        log: BoundLogger = kwargs.get("log", LOGGER.new())  # noqa: F841

        return DioptraResource.query.all()  # type: ignore

    @staticmethod
    def get_by_id(resource_id: int, **kwargs) -> DioptraResource:
        log: BoundLogger = kwargs.get("log", LOGGER.new())  # noqa: F841

        return DioptraResource.query.get(resource_id)  # type: ignore

    def submit(self, creator_id: int, owner_id: int,**kwargs) -> DioptraResource:
        log: BoundLogger = kwargs.get("log", LOGGER.new())  # noqa: F841
        new_resource: DioptraResource = self.create(creator_id, owner_id, **kwargs)

        db.session.add(new_resource)
        db.session.commit()

        log.info("DioptraResource submission successful", resource_id=new_resource.resource_id)

        return new_resource

    def delete(self, resource_id: int, **kwargs) -> bool:
        log: BoundLogger = kwargs.get("log", LOGGER.new())  # noqa: F841
        
        resource = self.get_by_id(resource_id)

        if resource:
            resource.is_deleted = True
            try:
                db.session.commit()
                log.info("DioptraResource deleted", resource_id=resource_id)
                return True
            except IntegrityError:
                db.session.rollback()
                log.error("Failed to delete DioptraResource", resource_id=resource_id)
                return False

        return False
