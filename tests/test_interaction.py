import pytest
import numpy as np
import os

import pandas as pd
import networkx as nx

from deployict.interactions import GraphCreator

tests_folder = "tests"
test_empty_file = "empty_file_for_testing_purpose.txt"
test_wrapper_file = "wrapper_for_testing_purpose.py"


@pytest.fixture()
def g(simulator=GraphCreator):
    sim = simulator()

    sim.add_meta(
        name="SimpleHP",
        set_attrs=["a1", "a2"],
        get_attrs=["b1", "b2"])

    sim.add_type(
        name="fmuHP",
        meta="SimpleHP",
        image="ict-python",
        wrapper=os.path.join(tests_folder, test_wrapper_file),
        command=["init_values.json"],
        files=[os.path.join(tests_folder, test_empty_file)])

    hps = {}
    for name in ["HP_{}".format(i) for i in range(3)]:
        hps[name] = sim.add_node(
            name=name,
            node_type="fmuHP",
            init_values={
                "p_nom": int(np.random.uniform(10, 500)),
                "mode": np.random.choice(["cooling", "heating"])})

    sim.add_multiple_links_between_two_nodes(hps["HP_0"], hps["HP_1"], ["b1", "b2"], ["a1", "a2"], ["kW", "deg.C"])
    sim.add_multiple_links_between_two_nodes(hps["HP_1"], hps["HP_2"], ["b1", "b2"], ["a1", "a2"], ["kW", "deg.C"])
    sim.add_multiple_links_between_two_nodes(hps["HP_2"], hps["HP_0"], ["b1", "b2"], ["a1", "a2"], ["kW", "deg.C"])

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


def test_returned_links_is_a_data_frame(g):
    _, links = g.data
    assert type(links) is pd.DataFrame


def test_graph_is_a_multi_directed_graph(g):
    assert type(g._graph) is nx.MultiDiGraph
