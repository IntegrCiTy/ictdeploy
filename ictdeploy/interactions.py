import networkx as nx
import pandas as pd


class Node:
    def __init__(self, name, model, init_values, is_first):
        self.name = name

        self.model = model
        self.init_values = init_values
        self.is_first = is_first

    def __repr__(self):
        return str(self.model) + " -> " + str(self.init_values)


def _empty_list_if_none(l):
    if l is None:
        l = []
    return l


class GraphCreator:
    def __init__(self):
        self.meta_models = {}
        self.models = {}
        self._graph = nx.MultiDiGraph()

    @property
    def nodes(self):
        return pd.DataFrame.from_dict(
            {
                node: {
                    "meta": self.models[data["node"].model]["meta"],
                    "model": data["node"].model,
                    "to_set": self.meta_models[self.models[data["node"].model]["meta"]]["set_attrs"],
                    "to_get": self.meta_models[self.models[data["node"].model]["meta"]]["get_attrs"],
                    "image": self.models[data["node"].model]["image"],
                    "wrapper": self.models[data["node"].model]["wrapper"],
                    "files": self.models[data["node"].model]["files"],
                    "command": self.models[data["node"].model]["command"],
                    "init_values": data["node"].init_values,
                    "is_first": data["node"].is_first
                } for node, data in self._graph.nodes(data=True)
            }, orient="index")

    @property
    def links(self):
        return pd.DataFrame(
            [
                {
                    "get_node": get_node,
                    "get_attr": data["link"]["get_attr"],
                    "set_node": set_node,
                    "set_attr": data["link"]["set_attr"]
                } for get_node, set_node, data in self._graph.edges(data=True)
            ])

    def add_meta(self, name, set_attrs=None, get_attrs=None):
        self.meta_models[name] = {
            'set_attrs': _empty_list_if_none(set_attrs),
            'get_attrs': _empty_list_if_none(get_attrs)
        }
        return name

    def add_model(self, name, meta, image, wrapper, command, files):
        self.models[name] = {
            'meta': meta,
            'image': image,
            'wrapper': wrapper,
            'command': command,
            'files': files
        }
        return name

    def add_node(self, name, model, init_values=None, is_first=False):
        if init_values is None:
            init_values = {}
        node = Node(name, model, init_values, is_first)
        self._graph.add_node(node.name, node=node)
        return node.name

    def add_link(self, get_node, set_node, get_attr, set_attr, unit="unit"):
        self._graph.add_edge(get_node, set_node, link={"get_attr": get_attr, "set_attr": set_attr, "unit": unit})

    def add_multiple_links_between_two_nodes(self, get_node, set_node, get_attrs, set_attrs, units=None):
        if not units:
            units = ["unit"] * len(get_attrs)
        for get_attr, set_attr, unit in zip(get_attrs, set_attrs, units):
            self.add_link(get_node, set_node, get_attr, set_attr, unit)

    @property
    def interaction_graph(self):
        return {
            "nodes": {node: {
                "inputs": row["to_set"],
                "outputs": row["to_get"]
            } for node, row in self.nodes.iterrows()},

            "links": {"Link_{}".format(i): {
                "out": {
                    "node": link["get_node"],
                    "attr": link["get_attr"]},
                "in": {
                    "node": link["set_node"],
                    "attr": link["set_attr"]}
            } for i, link in self.links.iterrows()}
        }
