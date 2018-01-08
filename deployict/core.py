from deployict.deployment import SimNodesCreator
from deployict.interactions import GraphCreator


# TODO: Add a logger
class Simulator(GraphCreator, SimNodesCreator):
    def __init__(self):
        super().__init__()

    def deploy_aux(self):
        pass

    def deploy_nodes(self, client=None):
        logs = {}
        for node in self.nodes:
            node_type = self.types[node.type]

            node_folder = self.create_volume(
                node.name,
                node.init_values,
                node_type["wrapper"],
                *node_type["files"]
            )

            print('COMMAND:', node_type["command"])

            logs[node.name] = self.deploy_node(
                node.name,
                node_type["image"],
                node_folder,
                node_type["wrapper"],
                command=node_type["command"],
                client=client
            )
        return logs

