import pandas as pd

from tests.common import clean_tmp_folder, clean_containers, get_logs
from tests.fixtures_test import fix_deploy


def test_list_of_available_results(fix_deploy):
    sim, logs_aux, logs_orc, logs = fix_deploy
    sim.connect_to_db()
    df = sim.list_of_available_results
    assert type(df) == pd.DataFrame
    assert set(list(df.columns)) == {'Node', 'IN/OUT', 'Attribute'}


def teardown_function():
    clean_tmp_folder()
    clean_containers()
