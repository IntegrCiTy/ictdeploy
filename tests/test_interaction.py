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
        node_type="fmuHP",
        init_values={
            "p_nom": int(np.random.uniform(10, 500)),
            "mode": np.random.choice(["cooling", "heating"])}
    )

    hp2 = sim.add_node(
        name="HP_2",
        node_type="fmuHP",
        init_values={
            "p_nom": int(np.random.uniform(10, 500)),
            "mode": np.random.choice(["cooling", "heating"])}
    )

    sim.add_multiple_links_between_two_nodes("HP_0", hp1, ["b1", "b2"], ["a1", "a2"], ["kW", "deg.C"])
    sim.add_multiple_links_between_two_nodes(hp1, hp2, ["b1", "b2"], ["a1", "a2"], ["kW", "deg.C"])
    sim.add_multiple_links_between_two_nodes(hp2, "HP_0", ["b1", "b2"], ["a1", "a2"], ["kW", "deg.C"])

    return sim


def test_number_of_created_nodes(g):
    nodes, _ = g.data
    assert len(nodes) == 3


def test_number_of_created_links(g):
    _, links = g.data
    assert len(links) == 6


def test_returned_nodes_is_a_data_frame(g):
    nodes, _ = g.data
    assert type(nodes) is pd.DataFrame


def test_returned_nodes(g):
    nodes, _ = g.data
    for _, row in nodes.iterrows():
        assert row["type"] == "fmuHP"
        assert row["meta"] == "SimpleHP"


def test_returned_links_is_a_data_frame(g):
    _, links = g.data
    assert type(links) is pd.DataFrame


def test_graph_is_a_multi_directed_graph(g):
    assert type(g._graph) is nx.MultiDiGraph


def test_interaction_graph(g):

    waited = {'links': {'Link_0': {'in': {'attr': 'a1', 'node': 'HP_0'},
                                   'out': {'attr': 'b1', 'node': 'HP_2'}},
                        'Link_1': {'in': {'attr': 'a2', 'node': 'HP_0'},
                                   'out': {'attr': 'b2', 'node': 'HP_2'}},
                        'Link_2': {'in': {'attr': 'a1', 'node': 'HP_1'},
                                   'out': {'attr': 'b1', 'node': 'HP_0'}},
                        'Link_3': {'in': {'attr': 'a2', 'node': 'HP_1'},
                                   'out': {'attr': 'b2', 'node': 'HP_0'}},
                        'Link_4': {'in': {'attr': 'a1', 'node': 'HP_2'},
                                   'out': {'attr': 'b1', 'node': 'HP_1'}},
                        'Link_5': {'in': {'attr': 'a2', 'node': 'HP_2'},
                                   'out': {'attr': 'b2', 'node': 'HP_1'}}},
              'nodes': {'HP_0': {'inputs': ['a1', 'a2'], 'outputs': ['b1', 'b2']},
                        'HP_1': {'inputs': ['a1', 'a2'], 'outputs': ['b1', 'b2']},
                        'HP_2': {'inputs': ['a1', 'a2'], 'outputs': ['b1', 'b2']}}}

    assert g.interaction_graph == waited
