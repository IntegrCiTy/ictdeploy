import os
import json
import pandas as pd
import networkx as nx

from tests.common import clean_tmp_folder
from tests.fixtures_test import fix_create, fix_volume


def test_returned_links_is_a_data_frame(fix_create):
    assert type(fix_create.edit.links) is pd.DataFrame


def test_graph_is_a_multi_directed_graph(fix_create):
    assert type(fix_create.edit.graph) is nx.MultiDiGraph


def test_number_of_created_nodes_is_correct(fix_create):
    assert len(fix_create.edit.nodes) == 2


def test_number_of_created_links_is_correct(fix_create):
    assert len(fix_create.edit.links) == 2


def test_returned_nodes_are_meaningful(fix_create):
    for _, row in fix_create.edit.nodes.iterrows():
        assert row["model"] == "BaseModel"
        assert row["meta"] == "BaseMeta"
        assert row["to_set"] == ["a"]
        assert row["to_get"] == ["b"]
        assert row["image"] == "integrcity/ict-simple"
        assert row["wrapper"] == os.path.join("tests", "wrappers", "base_wrap.py")
        assert row["files"] == [os.path.join("tests", "files_to_add", "empty_file_for_testing_purpose.txt")]
        assert row["command"] is None


def test_interaction_graph_links_and_nodes_number(fix_create):
    g_dict = fix_create.edit.interaction_graph
    assert len(g_dict["links"]) == 2
    assert len(g_dict["nodes"]) == 2


def test_steps_are_well_defined(fix_create):
    assert fix_create.steps == [60, 60, 60, 60, 60, 60, 60, 60, 60, 60]


def test_sequence_is_well_defined(fix_create):
    assert fix_create.sequence == [('Base0',), ('Base1',)]


def test_tmp_folder_is_created(fix_volume):
    assert os.path.isdir(fix_volume.deploy.TMP_FOLDER)


def test_nodes_folders_are_created(fix_volume):
    assert os.listdir(fix_volume.deploy.TMP_FOLDER) == ['Base0', 'Base1']


def test_basic_files_are_in_nodes_folders(fix_volume):
    for node in fix_volume.edit.nodes.index:
        files = ['empty_file_for_testing_purpose.txt', 'base_wrap.py', 'init_values.json', 'config_file.json']
        assert os.listdir(os.path.join(fix_volume.deploy.TMP_FOLDER, node)) == files


def test_init_values_file_contains_all_data(fix_volume):
    for node in fix_volume.edit.nodes.index:
        with open(os.path.join(fix_volume.deploy.TMP_FOLDER, node, "init_values.json")) as json_data:
            init_values = json.load(json_data)
        assert "c" in init_values


def test_node_config_file_contains_all_data(fix_volume):
    for node in fix_volume.edit.nodes.index:
        with open(os.path.join(fix_volume.deploy.TMP_FOLDER, node, "config_file.json")) as json_data:
            config_file = json.load(json_data)
        assert {"name", "queues", "exchanges"}.issubset(config_file)
        assert {"obnl.simulation.node.", "obnl.local.node.", "obnl.data.node."}.issubset(config_file["queues"])
        assert {"obnl.simulation.node.", "obnl.local.node."}.issubset(config_file["exchanges"])


def teardown_function():
    clean_tmp_folder()
