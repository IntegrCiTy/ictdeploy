import pytest

from tests.common import clean_tmp_folder, clean_containers


def test_number_of_nodes_containers():
    assert True
    # TODO: create test (or full demo) ?


def test_orchestrator_container_connected():
    assert True
    # TODO: create test (or full demo) ?


def teardown_function():
    clean_tmp_folder()
    clean_containers()
