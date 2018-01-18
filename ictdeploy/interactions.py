import networkx as nx
import pandas as pd


# TODO: find the WTF is going on with objects df
class Node:
    def __init__(self, name, node_type, init_values):
        self.name = name
        self.type = node_type
        self.init_values = init_values

    def __repr__(self):
        return str(self.name)


def empty_list_if_none(l):
    if l is None:
        l = []
    return l


class GraphCreator:
    def __init__(self):
        self.meta_models = {}
        self.types = {}
        self._graph = nx.MultiDiGraph()

    @property
    def nodes(self):
        return self._graph.nodes

    @property
    def links(self, data=True):
        return self._graph.edges(data=data)

    def _catch_node(self, node):
        if type(node) is not Node:
            node = [n for n in self.nodes if node is n.name][0]
        return node

    def add_meta(self, name, set_attrs=None, get_attrs=None):
        self.meta_models[name] = {
            'set_attrs': empty_list_if_none(set_attrs),
            'get_attrs': empty_list_if_none(get_attrs)
        }

    def add_type(self, name, meta, image, wrapper, command, files):
        self.types[name] = {
            'meta': meta,
            'image': image,
            'wrapper': wrapper,
            'command': command,
            'files': files
        }

    def add_node(self, name, node_type, init_values=None):
        if init_values is None:
            init_values = {}
        node = Node(name, node_type, init_values)
        self._graph.add_node(node)
        return node

    def add_link(self, get_node, set_node, get_attr, set_attr, unit):
        self._graph.add_edge(
            self._catch_node(get_node),
            self._catch_node(set_node),
            get_attr=get_attr,
            set_attr=set_attr,
            unit=unit
        )

    def add_multiple_links_between_two_nodes(self, get_node, set_node, get_attrs, set_attrs, units):
        for get_attr, set_attr, unit in zip(get_attrs, set_attrs, units):
            self.add_link(get_node, set_node, get_attr, set_attr, unit)

    @property
    def interaction_graph(self):
        nodes, links = self.data

        inter = {
            "nodes": {node: {
                "inputs": row["to_set"],
                "outputs": row["to_get"]
            } for node, row in nodes.iterrows()},

            "links": {"Link_{}".format(i): {
                "out": {
                    "node": link["get_node"],
                    "attr": link["get_attr"]},
                "in": {
                    "node": link["set_node"],
                    "attr": link["set_attr"]}
            } for i, link in links.iterrows()}
        }

        return inter

    @property
    def data(self):
        nodes_dict = {n.name: {
            "meta": self.types[n.type]["meta"],
            "type": n.type,
            "init_values": n.init_values,
            "to_set": self.meta_models[self.types[n.type]["meta"]]["set_attrs"],
            "to_get": self.meta_models[self.types[n.type]["meta"]]["get_attrs"],
            "wrapper": self.types[n.type]["wrapper"],
            "command": self.types[n.type]["command"]
        } for n in self.nodes}

        links_list = [{
            "get_node": get_node.name,
            "set_node": set_node.name,
            "get_attr": data["get_attr"],
            "set_attr": data["set_attr"],
            "unit": data["unit"]
        } for get_node, set_node, data in self.links]

        nodes = pd.DataFrame.from_dict(nodes_dict, orient="index")
        links = pd.DataFrame(links_list)
        return nodes, links
