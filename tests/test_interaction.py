import pytest
import numpy as np

import pandas as pd
import networkx as nx

from tests.fixtures import s_lsd


@pytest.fixture()
def g():
    sim = s_lsd()

    hp1 = sim.add_node(
        name="HP_1",
        model="fmuHP",
        init_values={
            "p_nom": int(np.random.uniform(10, 500)),
            "mode": np.random.choice(["cooling", "heating"])}
    )

    hp2 = sim.add_node(
        name="HP_2",
        model="fmuHP",
        init_values={
            "p_nom": int(np.random.uniform(10, 500)),
            "mode": np.random.choice(["cooling", "heating"])}
    )

    sim.add_multiple_links_between_two_nodes("HP_0", hp1, ["b1", "b2"], ["a1", "a2"], ["kW", "deg.C"])
    sim.add_multiple_links_between_two_nodes(hp1, hp2, ["b1", "b2"], ["a1", "a2"], ["kW", "deg.C"])
    sim.add_multiple_links_between_two_nodes(hp2, "HP_0", ["b1", "b2"], ["a1", "a2"], ["kW", "deg.C"])

    return sim


def test_number_of_created_nodes(g):
    assert len(g.nodes) == 3


def test_number_of_created_links(g):
    assert len(g.links) == 6


def test_returned_nodes_is_a_data_frame(g):
    assert type(g.nodes) is pd.DataFrame


def test_returned_nodes(g):
    for _, row in g.nodes.iterrows():
        assert row["model"] == "fmuHP"
        assert row["meta"] == "SimpleHP"


def test_returned_links_is_a_data_frame(g):
    assert type(g.links) is pd.DataFrame


def test_graph_is_a_multi_directed_graph(g):
    assert type(g._graph) is nx.MultiDiGraph


def test_interaction_graph(g):
    g_dict = g.interaction_graph
    assert len(g_dict["links"]) == 6
    assert len(g_dict["nodes"]) == 3
