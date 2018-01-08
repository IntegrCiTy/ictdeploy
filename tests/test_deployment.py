import pytest

import os
import shutil

from deployict.deployment import SimNodesCreator as Sim

tests_folder = "tests"
test_empty_file = "empty_file_for_testing_purpose.txt"
test_wrapper_file = "wrapper_for_testing_purpose.py"


def print_logs(logs):
    outputs = []
    while True:
        try:
            outputs.append(logs.__next__().decode("utf-8").rstrip())
        except StopIteration:
            break
    return outputs


@pytest.fixture()
def s():
    sim = Sim()
    node_folder = sim.create_volume(
        "node_1",
        {"a": 0},
        os.path.join(tests_folder, test_empty_file),
        os.path.join(tests_folder, test_wrapper_file)
    )

    return sim, node_folder


@pytest.fixture()
def s_deploy():
    sim, node_folder = s()

    logs = sim.deploy_node(
        node_name="node_1",
        image="ict-python",
        node_folder=node_folder,
        wrapper=test_wrapper_file,
    )

    return sim, node_folder, logs


def test_created_folder_exist(s):
    _, node_folder = s
    assert os.path.isdir(node_folder)


def test_init_values_file_exists(s):
    _, node_folder = s
    assert os.path.isfile(os.path.join(node_folder, Sim.INIT_VALUES_FILE))


def test_added_file_exists(s):
    _, node_folder = s
    assert os.path.isfile(os.path.join(node_folder, test_empty_file))


def test_container_exist(s_deploy):
    sim, _, _ = s_deploy
    assert "node_1" in [c.name for c in sim.CLIENT.containers.list()]


def test_logs_init_values(s_deploy):
    _, _, logs = s_deploy
    outputs = print_logs(logs)
    assert "initial values -> {'a': 0}" in outputs


def teardown_function():
    shutil.rmtree(Sim.TMP_FOLDER)

    Sim.CLIENT.containers.prune()

    for container in Sim.CLIENT.containers.list():
        container.kill()
