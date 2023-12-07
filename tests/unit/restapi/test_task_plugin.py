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

import tarfile
from typing import Any, BinaryIO, Dict

import pytest
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from werkzeug.test import TestResponse

from dioptra.restapi.task_plugin.routes import BASE_ROUTE as TASK_PLUGIN_BASE_ROUTE


# -- Fixtures --------------------------------------------------------------------------


@pytest.fixture
def task_plugin_builtin_request_form(task_plugin_archive: BinaryIO) -> Dict[str, Any]:
    return {
        "task_plugin_name": "builtin_plugin",
        "task_plugin_file": (task_plugin_archive, "task_plugin_new_builtin_package.tar.gz"),
        "collection": "dioptra_builtins"
    }

@pytest.fixture
def task_plugin_custom_request_form(task_plugin_archive: BinaryIO) -> Dict[str, Any]:
    return {
        "task_plugin_name": "custom_plugin",
        "task_plugin_file": (task_plugin_archive, "task_plugin_new_custom_package.tar.gz"),
        "collection": "dioptra_custom"
    }


# -- Actions ---------------------------------------------------------------------------


def register_task_plugin(
    client: FlaskClient,
    task_plugin_request_form: Dict[str, Any],
) -> TestResponse:
    """Register a task plugin package using the API.

    Args:
        client: The Flask test client.
        task_plugin_name: The name to assign to the new task plugin package.
        task_plugin_file: A tarball archive or zip file containing a single task plugin
        collection: The collection where the task plugin should be stored.


    Returns:
        The response from the API.
    """
    return client.post(
        f"/api/{TASK_PLUGIN_BASE_ROUTE}/",
        data=task_plugin_request_form,
        follow_redirects=True,
    )


def delete_custom_task_plugin_with_name(
    client: FlaskClient,
    task_plugin_name: str,
) -> TestResponse:
    """Delete a custom task plugin using the API.

    Args:
        client: The Flask test client.
        task_plugin_name: The name of the custom task plugin to delete.

    Returns:
        The response from the API.
    """
    return client.delete(
        f"/api/{TASK_PLUGIN_BASE_ROUTE}/dioptra_custom/{task_plugin_name}",
        follow_redirects=True,
    )


# -- Assertions ------------------------------------------------------------------------


def assert_retrieving_builtins_task_plugin_by_name_works(
    client: FlaskClient,
    task_plugin_name: str,
    expected: dict[str, Any],
) -> None:
    """Assert that retrieving a builtin task plugin by name works.

    Args:
        client: The Flask test client.
        task_plugin_name: The name of the builtin task plugin to retrieve.
        expected: The expected response from the API.

    Raises:
        AssertionError: If the response status code is not 200 or if the API response
            does not match the expected response.
    """
    response = client.get(
        f"/api/{TASK_PLUGIN_BASE_ROUTE}/dioptra_builtins/{task_plugin_name}", follow_redirects=True
    )
    assert response.status_code == 200 and response.get_json() == expected


def assert_retrieving_custom_task_plugin_by_name_works(
    client: FlaskClient,
    task_plugin_name: str,
    expected: dict[str, Any],
) -> None:
    """Assert that retrieving a custom task plugin by name works.

    Args:
        client: The Flask test client.
        task_plugin_name: The name of the custom task plugin to retrieve.
        expected: The expected response from the API.

    Raises:
        AssertionError: If the response status code is not 200 or if the API response
            does not match the expected response.
    """
    response = client.get(
        f"/api/{TASK_PLUGIN_BASE_ROUTE}/dioptra_custom/{task_plugin_name}", follow_redirects=True
    )
    assert response.status_code == 200 and response.get_json() == expected


def assert_retrieving_all_builtins_task_plugins_works(
    client: FlaskClient,
    expected: list[dict[str, Any]],
) -> None:
    """Assert that retrieving all builtin task plugins works.

    Args:
        client: The Flask test client.
        expected: The expected response from the API.

    Raises:
        AssertionError: If the response status code is not 200 or if the API response
            does not match the expected response.
    """
    response = client.get(f"/api/{TASK_PLUGIN_BASE_ROUTE}/dioptra_builtins", follow_redirects=True)
    assert response.status_code == 200 and response.get_json() == expected


def assert_retrieving_all_custom_task_plugins_works(
    client: FlaskClient,
    expected: list[dict[str, Any]],
) -> None:
    """Assert that retrieving all custom task plugins works.

    Args:
        client: The Flask test client.
        expected: The expected response from the API.

    Raises:
        AssertionError: If the response status code is not 200 or if the API response
            does not match the expected response.
    """
    response = client.get(f"/api/{TASK_PLUGIN_BASE_ROUTE}/dioptra_custom", follow_redirects=True)
    assert response.status_code == 200 and response.get_json() == expected


def assert_retrieving_all_task_plugins_works(
    client: FlaskClient,
    expected: list[dict[str, Any]],
) -> None:
    """Assert that retrieving all task plugins works.

    Args:
        client: The Flask test client.
        expected: The expected response from the API.

    Raises:
        AssertionError: If the response status code is not 200 or if the API response
            does not match the expected response.
    """
    response = client.get(f"/api/{TASK_PLUGIN_BASE_ROUTE}", follow_redirects=True)
    assert response.status_code == 200 and response.get_json() == expected


def assert_registering_existing_task_plugin_name_fails(
    client: FlaskClient, 
    task_plugin_request_form: Dict[str, Any],
) -> None:
    """Assert that registering a task plugin with an existing name in the same collection fails.

    Args:
        client: The Flask test client.
        name: The name to assign to the new queue.

    Raises:
        AssertionError: If the response status code is not 400.
    """
    response = register_task_plugin(client, task_plugin_request_form)
    assert response.status_code == 400


def assert_custom_task_plugin_not_found(
    client: FlaskClient,
    task_plugin_name: str,
) -> None:
    """Assert that a task plugin package is not found.

    Args:
        client: The Flask test client.
        queue_id: The id of the queue to retrieve.

    Raises:
        AssertionError: If the response status code is not 404.
    """
    response = client.get(
        f"/api/{TASK_PLUGIN_BASE_ROUTE}/dioptra_custom/{task_plugin_name}",
        follow_redirects=True,
    )
    assert response.status_code == 404


# -- Tests -----------------------------------------------------------------------------


def test_task_plugin_registration(
    client: FlaskClient,
    db: SQLAlchemy,
    task_plugin_builtin_request_form: Dict[str, Any],
    task_plugin_custom_request_form: Dict[str, Any],
) -> None:
    """Test that task plugin packages can be registered and retrieved using the API.

    This test validates the following sequence of actions:

    - A user registers a builtin task plugin package and a custom task plugins package.
    - The user is able to retrieve information about each task plugin package using its unique name.
    - The user is able to retrieve a list of all registered builtin task plugin packages.
    - The user is able to retrieve a list of all registered custom task plugin packages.
    - The user is able to retrieve a list of all registered task plugin packages.
    - In all cases, the returned information matches the information that was provided
      during registration.
    """

    plugin1_response = register_task_plugin(client, task_plugin_builtin_request_form)
    plugin2_response = register_task_plugin(client, task_plugin_custom_request_form)
    plugin1_expected = plugin1_response.get_json()
    plugin2_expected = plugin2_response.get_json()
    builtins_expected_list = [plugin1_expected]
    custom_expected_list = [plugin2_expected]
    all_expected_list = [plugin1_expected, plugin2_expected]
    assert_retrieving_builtins_task_plugin_by_name_works(
        client, task_plugin_name=plugin1_expected["taskPluginName"], expected=plugin1_expected
    )
    assert_retrieving_builtins_task_plugin_by_name_works(
        client, task_plugin_name=plugin2_expected["taskPluginName"], expected=plugin2_expected
    )
    assert_retrieving_all_builtins_task_plugins_works(client, expected=builtins_expected_list)
    assert_retrieving_all_custom_task_plugins_works(client, expected=custom_expected_list)
    assert_retrieving_all_task_plugins_works(client, expected=all_expected_list)


def test_cannot_register_existing_task_plugin_name(
    client: FlaskClient,
    db: SQLAlchemy,
    task_plugin_builtin_request_form: Dict[str, Any],
    task_plugin_custom_request_form: Dict[str, Any],
) -> None:
    """Test that registering a task plugin package with an existing name fails.

    This test validates the following sequence of actions:

    - A user registers a builtin task plugin.
    - A user registers a custom task plugin.
    - The user attempts to register a second builtin task plugin with the same name, which fails.
    - The user attempts to register a second custom task plugin with the same name, which fails.
    """

    register_task_plugin(client, task_plugin_builtin_request_form)
    register_task_plugin(client, task_plugin_custom_request_form)
    assert_registering_existing_task_plugin_name_fails(client, task_plugin_builtin_request_form)
    assert_registering_existing_task_plugin_name_fails(client, task_plugin_custom_request_form)

def test_delete_custom_task_plugin_by_name(
    client: FlaskClient,
    db: SQLAlchemy,
    task_plugin_custom_request_form: Dict[str, Any],
) -> None:
    """Test that a task plugin can be deleted by referencing its name.

    This test validates the following sequence of actions:

    - A user registers a task plugin.
    - The user is able to retrieve information about the task plugin that
      matches the name that was provided during registration.
    - The user deletes the task plugin by referencing its name.
    - The user attempts to retrieve information about the task plugin by name, which
      is no longer found.
    """

    registration_response = register_task_plugin(client, task_plugin_custom_request_form)
    task_plugin_json = registration_response.get_json()
    assert_retrieving_custom_task_plugin_by_name_works(
        client, task_plugin_name=task_plugin_json["taskPluginName"], expected=task_plugin_json
    )
    delete_custom_task_plugin_with_name(client, task_plugin_name=task_plugin_json["taskPluginName"])
    assert_custom_task_plugin_not_found(client, task_plugin_name=task_plugin_json["taskPluginName"])
