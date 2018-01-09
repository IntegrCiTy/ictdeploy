import pytest

import shutil
import os

from deployict import Simulator as Sim
from tests.test_interaction import g


@pytest.fixture()
def s():
    sim = g(Sim)
    logs = sim.deploy_nodes()
    return sim, logs


def test_number_of_containers(s):
    _, logs = s
    assert len(logs) == 3


def teardown_function():
    if os.path.isdir(Sim.TMP_FOLDER):
        shutil.rmtree(Sim.TMP_FOLDER)

    Sim.CLIENT.containers.prune()

    for container in Sim.CLIENT.containers.list():
        container.kill()
