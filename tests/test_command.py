import pytest
from os.path import join
from ast import literal_eval

from ictdeploy import Simulator as Sim
from tests.common import tests_folder, wraps_folder
from tests.common import clean_tmp_folder, clean_containers, get_logs


wrap_cmd = "wrap_cmd.py"
image = "ict-base"


@pytest.fixture()
def f():
    sim = Sim()

    sim.edit.add_meta(name="SimpleHP", set_attrs=["a1", "a2"], get_attrs=["b1", "b2"])

    sim.edit.add_model(
        name="fmuHP",
        meta="SimpleHP",
        image=image,
        wrapper=join(tests_folder, wraps_folder, wrap_cmd),
        command="hp.fmu",
        files=[],
    )

    sim.edit.add_node(
        name="HP_0",
        model="fmuHP",
        is_first=True,
        init_values={"p_nom": 100, "mode": "heating"},
    )

    return sim


def test_wrapper_received_command(f):
    sim = f
    logs = sim.deploy_nodes()
    logs = get_logs(logs["HP_0"])
    str_logs = "".join(str(elem) for elem in logs)

    waited = {
        "--first": True,
        "--help": False,
        "--i": ["a1", "a2"],
        "--o": ["b1", "b2"],
        "--version": False,
        "-h": False,
        "--cmd": "hp.fmu",
        "<host>": "172.17.01",
        "<init>": "init_values.json",
        "<name>": "HP_0",
    }

    assert waited.items() == literal_eval(str_logs).items()


def teardown_function():
    clean_tmp_folder()
    clean_containers()
