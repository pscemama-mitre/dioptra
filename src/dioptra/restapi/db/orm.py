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
from __future__ import annotations

from functools import wraps
from typing import Any, Callable, TypeVar, cast

from sqlalchemy.orm import registry, relationship

Function = Callable[..., Any]
T = TypeVar("T", bound=Function)


def run_once(func: T) -> T:
    function_called_previously = False

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal function_called_previously

        if function_called_previously:
            return None

        func_output = func(*args, **kwargs)
        function_called_previously = True
        return func_output

    return cast(T, wrapper)


@run_once
def register_orm_mappings(mapper_registry: registry):
    from .models import Queue, QueueLock
    from .tables import queue_locks_table, queues_table

    mapper_registry.map_imperatively(
        QueueLock,
        queue_locks_table,
        properties={
            "queue": relationship(Queue, back_populates="lock"),
        },
    )
    mapper_registry.map_imperatively(
        Queue,
        queues_table,
        properties={
            "jobs": relationship("Job", back_populates="queue", lazy="dynamic"),
            "lock": relationship(QueueLock, back_populates="queue"),
        },
    )
