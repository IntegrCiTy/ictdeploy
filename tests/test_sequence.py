import pytest
from tests.test_interaction import g


@pytest.fixture()
def gg():
    sim = g()
    grp0 = sim.create_group("HP_0")
    grp1 = sim.create_group("HP_1")
    grp2 = sim.create_group("HP_2")
    sim.create_sequence(grp0, grp1, grp2)
    return sim


def test_sequence_length(gg):
    sim = gg
    assert len(sim.sequence) == 3
