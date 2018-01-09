import pytest

from tests.test_interaction import g
from tests.common import clean_tmp_folder, clean_containers


@pytest.fixture()
def s():
    sim = g()
    logs = sim.deploy_nodes()
    return sim, logs


def test_number_of_containers(s):
    _, logs = s
    assert len(logs) == 3


def teardown_function():
    clean_tmp_folder()
    clean_containers()
