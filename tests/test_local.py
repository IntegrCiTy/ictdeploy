import os
import pytest

from tests.common import clean_tmp_folder, clean_containers, get_logs
from ictdeploy import Simulator as Sim


@pytest.fixture()
def fix_local():
    """
    Fixture for testing purpose creating a ready-to-run simple co-simulation

    :return: ictdeploy.Simulator() with meta, models, nodes, links, groups, sequence and steps implemented
    """
    sim = Sim()

    sim.edit.add_meta(name="BaseMeta", set_attrs=["a"], get_attrs=["b"])

    sim.edit.add_model(
        name="BaseModel",
        meta="BaseMeta",
        image="integrcity/ict-simple",
        wrapper=os.path.join("tests", "wrappers", "base_wrap.py"),
        command=None,
        files=[
            os.path.join("tests", "files_to_add", "empty_file_for_testing_purpose.txt")
        ],
    )

    sim.edit.add_node(
        name="Base0", model="BaseModel", init_values={"c": 0.5}, is_first=True
    )

    sim.edit.add_node(
        name="Base1", model="BaseModel", init_values={"c": 0.25}, is_local=True
    )

    sim.edit.add_link(get_node="Base0", get_attr="b", set_node="Base1", set_attr="a")
    sim.edit.add_link(get_node="Base1", get_attr="b", set_node="Base0", set_attr="a")

    grp0 = sim.create_group("Base0")
    grp1 = sim.create_group("Base1")

    sim.create_sequence(grp0, grp1)
    sim.create_steps([60] * 10)

    sim.deploy_aux()
    sim.deploy_orchestrator(server=os.path.join("tests", "server.py"))

    return sim.deploy_nodes()


def test_local_not_deployed(fix_local):
    logs = fix_local
    assert logs["Base1"] is None


def teardown_function():
    clean_tmp_folder()
    clean_containers()
