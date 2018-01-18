import pytest

from tests.test_interaction import g
from tests.common import clean_tmp_folder, clean_containers, get_logs


@pytest.fixture()
def s():
    sim = g()
    logs = sim.deploy_nodes()
    return sim, logs


@pytest.fixture()
def s_obnl():
    sim = g()
    logs_aux = sim.deploy_aux()
    logs_orc = sim.deploy_orchestrator()
    return sim, logs_aux, logs_orc


def test_number_of_nodes_containers(s):
    _, logs = s
    assert len(logs) == 3


def test_orchestrator_container(s_obnl):
    sim, aux_logs, orc_logs = s_obnl
    waited = "['empty_file_for_testing_purpose.txt', 'wrap_listdir.py', 'init_values.json']"
    for xxx in get_logs(orc_logs):
        print("-->", xxx)
    # assert waited in get_logs(orc_logs)


def teardown_function():
    clean_tmp_folder()
    clean_containers()
