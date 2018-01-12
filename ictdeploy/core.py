from ictdeploy.deployment import SimNodesCreator
from ictdeploy.interactions import GraphCreator

# TODO: set up correctly logger
# from ictdeploy.logs import my_logger

# TODO: Set up images and modify code to allow defining wrapper in cmd (entrypoint: python)
# TODO: Create base python image with dedicated env


class Simulator(GraphCreator, SimNodesCreator):
    def __init__(self):
        super().__init__()

    def deploy_aux(self):
        pass

    def deploy_nodes(self, client=None):
        logs = {}

        nodes, _ = self.data

        for node_name, row in nodes.iterrows():
            node_type = self.types[row["type"]]

            node_folder = self.create_volume(
                node_name,
                row["init_values"],
                node_type["wrapper"],
                *node_type["files"]
            )

            logs[node_name] = self.deploy_node(
                node_name=node_name,
                image=node_type["image"],
                node_folder=node_folder,
                wrapper=node_type["wrapper"],
                command=node_type["command"],
                client=client
            )
        return logs
