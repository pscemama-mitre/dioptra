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
"""Test suite for queue operations.

This module contains a set of tests that validate the CRUD operations and additional
functionalities for the queue entity. The tests ensure that the queues can be
registered, renamed, deleted, and locked/unlocked as expected through the REST API.
"""
from __future__ import annotations

from typing import Any

from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from werkzeug.test import TestResponse

from dioptra.restapi.job.routes import BASE_ROUTE as JOB_BASE_ROUTE

# -- Actions ---------------------------------------------------------------------------


def register_job(
        client: FlaskClient, 
        experiment_name: str, 
        queue: str, 
        timeout: str,
        entry_point: str,
        entry_point_kwargs: str,
        depends_on: str,
        workflow: Any,

    ) -> TestResponse:
    """Register a job using the API.

    Args:
        client: The Flask test client.
        experiment_name: The name of a registered experiment.
        queue: The name of an active queue.
        timeout: The maximum alloted time for a job before it times out and is stopped. 
            If omitted, the job timeout will default to 24 hours.
        entry_point: The name of the entry point to run.
        entry_point_kwargs: A list of entry point parameter values to use for the job. 
            The list is a string with the following format: 
            -P param1=value1
            -P param2=value2
        depends_on: A job UUID to set as a dependency for this new job. The new job will not 
            run until this job completes successfully. If omitted, then the new job will start as 
            soon as computing resources are available.
        workflow: A tarball archive or zip file containing the entry point scripts.


    Returns:
        The response from the API.
    """
    return client.post(
        f"/api/{JOB_BASE_ROUTE}/",
        json={
            "experiment_name": experiment_name,
            "queue" : queue,
            "timeout" : timeout,
            "entry_point" : entry_point,
            "entry_point_kwargs" : entry_point_kwargs,
            "depends_on" : depends_on,
            "workflow" : workflow,
        },
        follow_redirects=True,
    )


# -- Assertions ------------------------------------------------------------------------





# -- Tests -----------------------------------------------------------------------------


