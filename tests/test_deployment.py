from tests.common import clean_tmp_folder, clean_containers, get_logs
from tests.fixtures_test import fix_deploy


def test_simulation_run(fix_deploy):
    sim, logs_aux, logs_orc, logs = fix_deploy
    assert len([l for l in get_logs(logs_orc) if "Simulation finished." in l]) == 1


def test_aux_containers_status(fix_deploy):
    sim, _, _, _ = fix_deploy
    assert sim.CLIENT.containers.get('ict_rab').status == "running"
    assert sim.CLIENT.containers.get('ict_red').status == "running"


def teardown_function():
    clean_tmp_folder()
    clean_containers()
