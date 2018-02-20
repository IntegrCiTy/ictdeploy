import os
import pytest
from ictdeploy import Simulator as Sim


@pytest.fixture()
def fix_create():
    sim = Sim()

    sim.add_meta(
        name="BaseMeta",
        set_attrs=["a"],
        get_attrs=["b"]
    )

    sim.add_model(
        name="BaseModel",
        meta="BaseMeta",
        image="ict-simple",
        wrapper=os.path.join("tests", "wrappers", "base_wrap.py"),
        command=None,
        files=[os.path.join("tests", "files_to_add", "empty_file_for_testing_purpose.txt")]
    )

    sim.add_node(
        name="Base0",
        model="BaseModel",
        init_values={"c": 0.5},
        is_first=True
    )

    sim.add_node(
        name="Base1",
        model="BaseModel",
        init_values={"c": 0.25}
    )

    sim.add_link(get_node="Base0", get_attr="b", set_node="Base1", set_attr="a")
    sim.add_link(get_node="Base1", get_attr="b", set_node="Base0", set_attr="a")

    grp0 = sim.create_group("Base0")
    grp1 = sim.create_group("Base1")

    sim.create_sequence(grp0, grp1)
    sim.create_steps([60] * 10)

    return sim


@pytest.fixture()
def fix_volume():
    sim = fix_create()

    for node_name, node in sim.nodes.iterrows():
        sim.create_volume(
            node_name,
            node["init_values"],
            node["wrapper"],
            *node["files"]
        )

    return sim


@pytest.fixture()
def fix_deploy():
    sim = fix_create()

    logs_aux = sim.deploy_aux()
    logs_orc = sim.deploy_orchestrator()
    logs = sim.deploy_nodes()

    return logs_aux, logs_orc, logs
