import pytest
from os.path import join
import numpy as np

from ictdeploy import Simulator as Sim
from tests.common import tests_folder, files_folder, wraps_folder


wrap_cmd = "wrap_cmd.py"
wrap_lsd = "wrap_listdir.py"
cmd = ["aaa", "bbb"]
file = "empty_file_for_testing_purpose.txt"

image = "ict-base"


@pytest.fixture()
def s_cmd():

    sim = Sim()

    sim.add_meta(
        name="SimpleHP",
        set_attrs=["a1", "a2"],
        get_attrs=["b1", "b2"]
    )

    sim.add_type(
        name="fmuHP",
        meta="SimpleHP",
        image=image,
        wrapper=join(tests_folder, wraps_folder, wrap_cmd),
        command=cmd,
        files=[join(tests_folder, files_folder, file)]
    )

    sim.add_node(
        name="HP_0",
        node_type="fmuHP",
        init_values={
            "p_nom": int(np.random.uniform(10, 500)),
            "mode": np.random.choice(["cooling", "heating"])}
    )

    return sim


@pytest.fixture()
def s_lsd():

    sim = Sim()

    sim.add_meta(
        name="SimpleHP",
        set_attrs=["a1", "a2"],
        get_attrs=["b1", "b2"]
    )

    sim.add_type(
        name="fmuHP",
        meta="SimpleHP",
        image=image,
        wrapper=join(tests_folder, wraps_folder, wrap_lsd),
        command=None,
        files=[join(tests_folder, files_folder, file)]
    )

    sim.add_node(
        name="HP_0",
        node_type="fmuHP",
        init_values={
            "p_nom": int(np.random.uniform(10, 500)),
            "mode": np.random.choice(["cooling", "heating"])}
    )

    return sim
