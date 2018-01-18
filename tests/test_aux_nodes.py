import pytest

from tests.common import clean_containers
from ictdeploy import Simulator as Sim


@pytest.fixture()
def aux():
    sim = Sim()
    logs = sim.deploy_aux()
    return sim, logs


def test_number_of_aux_containers(aux):
    _, logs = aux
    assert len(logs) == 2


def test_aux_containers_status(aux):
    sim, _ = aux

    rab = sim.CLIENT.containers.get('ict-rab')
    red = sim.CLIENT.containers.get('ict-red')

    assert rab.status == "running"
    assert red.status == "running"


def teardown_function():
    clean_containers()
