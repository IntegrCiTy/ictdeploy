from tests.common import clean_tmp_folder, clean_containers, get_logs
from tests.fixtures import s_lsd


def test_needed_files_are_in_container(s_lsd):
    sim = s_lsd
    logs = sim.deploy_nodes()
    waited = "['empty_file_for_testing_purpose.txt', 'wrap_listdir.py', 'init_values.json']"
    assert waited in get_logs(logs["HP_0"])


def teardown_function():
    clean_tmp_folder()
    clean_containers()
