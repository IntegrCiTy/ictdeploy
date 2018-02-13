import pytest

import os

from ictdeploy import Simulator as Sim

from tests.common import clean_tmp_folder
from tests.common import tests_folder, files_folder, wraps_folder
from tests.fixtures import wrap_lsd, file


@pytest.fixture()
def s():
    sim = Sim()

    wrapper = os.path.join(tests_folder, wraps_folder, wrap_lsd)
    useless_file = os.path.join(tests_folder, files_folder, file)

    node_folder = sim.create_volume("node", {"a": 0}, wrapper, useless_file)
    return sim, node_folder


def test_created_folder_exist(s):
    _, node_folder = s
    assert os.path.isdir(node_folder)


def test_added_files_exists(s):
    _, node_folder = s
    waited = [file, wrap_lsd, Sim.INIT_VALUES_FILE, Sim.CONFIG_FILE]
    assert os.listdir(node_folder) == waited


def teardown_function():
    clean_tmp_folder()
