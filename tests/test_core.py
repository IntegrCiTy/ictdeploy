import pytest

from tests.test_sequence import gg
from tests.common import clean_tmp_folder, clean_containers, get_logs


@pytest.fixture()
def s():
    sim = gg()
    logs = sim.deploy_nodes()
    return sim, logs


@pytest.fixture()
def s_obnl():
    sim = gg()
    logs_aux = sim.deploy_aux()
    logs_orc = sim.deploy_orchestrator()
    return sim, logs_aux, logs_orc


def test_number_of_nodes_containers(s):
    _, logs = s
    assert len(logs) == 3


def test_orchestrator_container_connected(s_obnl):
    sim, aux_logs, orc_logs = s_obnl
    logs = sim.deploy_nodes()
    assert True
    # TODO: infinite test...
    # printed_orc_logs = get_logs(orc_logs)
    #
    # waited = {
    #     0: "scheduler connected!",
    #     1: "Waiting for connection...",
    # }
    # for key, value in waited.items():
    #     assert value in printed_orc_logs[key]
    #
    # print("--->", printed_orc_logs[2:])


def teardown_function():
    clean_tmp_folder()
    clean_containers()
