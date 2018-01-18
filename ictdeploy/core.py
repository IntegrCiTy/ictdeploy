from ictdeploy.deployment import SimNodesCreator
from ictdeploy.interactions import GraphCreator
import time

# TODO: set up correctly logger
# from ictdeploy.logs import my_logger


class Simulator(GraphCreator, SimNodesCreator):
    def __init__(self):
        super().__init__()

    def deploy_aux(self, client=None):
        if client is None:
            client = self.CLIENT

        client.containers.run('redis:alpine',
                              name='ict-red',
                              ports={'6379/tcp': 6379},
                              detach=True,
                              auto_remove=True)

        client.containers.run('integrcity/rabbitmq',
                              name='ict-rab',
                              ports={'5672/tcp': 5672},
                              detach=True,
                              auto_remove=True)

        time.sleep(2)

        red_logs = client.containers.get("ict-red").logs(stream=True)
        rab_logs = client.containers.get("ict-rab").logs(stream=True)

        return {"ict-red": red_logs, "ict-rab": rab_logs}

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
