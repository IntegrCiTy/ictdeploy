import os
import pytest
from ictdeploy import Simulator as Sim


@pytest.fixture()
def fix_create():
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
        files=[os.path.join("tests", "files_to_add", "empty_file_for_testing_purpose.txt")],
    )

    sim.edit.add_node(name="Base0", model="BaseModel", init_values={"c": 0.5}, is_first=True)

    sim.edit.add_node(name="Base1", model="BaseModel", init_values={"c": 0.25})

    sim.edit.add_link(get_node="Base0", get_attr="b", set_node="Base1", set_attr="a")
    sim.edit.add_link(get_node="Base1", get_attr="b", set_node="Base0", set_attr="a")

    grp0 = sim.create_group("Base0")
    grp1 = sim.create_group("Base1")

    sim.create_sequence(grp0, grp1)
    sim.create_steps([60] * 10)

    return sim


@pytest.fixture()
def fix_volume():
    """
    Fixture for testing purpose based on fix_create() creating the local temporary folder to be mounted into containers

    :return: ictdeploy.Simulator() with local folders created for each node
    """
    sim = fix_create()

    for node_name, node in sim.edit.nodes.iterrows():
        sim.deploy.create_volume(node_name, node["init_values"], node["wrapper"], *node["files"])

    return sim


@pytest.fixture()
def fix_deploy():
    """
    Fixture for testing purpose based on fix_create() deploying all nodes and starting simulation

    :return: ictdeploy.Simulator() with simulation running and auxiliary nodes, orchestrator, and simulation nodes logs
    """
    sim = fix_create()

    logs_aux = sim.deploy_aux()
    logs_orc = sim.deploy_orchestrator()
    logs = sim.deploy_nodes()

    return sim, logs_aux, logs_orc, logs
