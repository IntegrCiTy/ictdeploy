import pandas as pd

from tests.common import clean_tmp_folder, clean_containers, get_logs
from tests.fixtures_test import fix_deploy


def test_the_list_of_available_simulation_results(fix_deploy):
    sim, logs_aux, logs_orc, logs = fix_deploy
    assert len([l for l in get_logs(logs_orc) if "Simulation finished." in l]) == 1
    sim.results.connect_to_results_db()
    df = sim.results.list_of_available_results
    assert type(df) == pd.DataFrame
    assert set(list(df.columns)) == {'Node', 'IN/OUT', 'Attribute'}
    assert len(df.index) == 4


def test_getting_simulation_results_by_pattern(fix_deploy):
    sim, logs_aux, logs_orc, logs = fix_deploy
    assert len([l for l in get_logs(logs_orc) if "Simulation finished." in l]) == 1
    sim.results.connect_to_results_db()
    res = sim.results.get_results_by_pattern("IN*Base0*")
    assert set(res) == {"IN||Base0||a"}
    assert type(res["IN||Base0||a"]) == pd.Series
    assert len(res["IN||Base0||a"].index) == 9


def teardown_function():
    clean_tmp_folder()
    clean_containers()
