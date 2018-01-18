from ictdeploy.deployment import SimNodesCreator
from ictdeploy.interactions import GraphCreator

import time
import json
import os


# TODO: set up correctly logger
# from ictdeploy.logs import my_logger


class Simulator(GraphCreator, SimNodesCreator):
    SCE_JSON_FILE = "interaction_graph.json"
    RUN_JSON_FILE = "sequences_and_steps.json"

    def __init__(self):
        super().__init__()

    def deploy_aux(self, client=None):
        """Deploy Redis (results database) and RabbitMQ (communication) containers"""
        if client is None:
            client = self.CLIENT

        client.containers.run(
            'redis:alpine',
            name='ict-red',
            ports={'6379/tcp': 6379},
            detach=True,
            auto_remove=True)

        client.containers.run(
            'integrcity/rabbitmq',
            name='ict-rab',
            ports={'5672/tcp': 5672},
            detach=True,
            auto_remove=True)

        time.sleep(2)

        red_logs = client.containers.get("ict-red").logs(stream=True)
        rab_logs = client.containers.get("ict-rab").logs(stream=True)

        return {"ict-red": red_logs, "ict-rab": rab_logs}

    def deploy_orchestrator(self, client=None):
        """Deploy and configure OBNL (orchestration) container"""
        if client is None:
            client = self.CLIENT

        obnl_folder = os.path.join(self.TMP_FOLDER, "obnl_folder")
        os.makedirs(obnl_folder)

        with open(os.path.join(obnl_folder, self.SCE_JSON_FILE), 'w') as fp:
            json.dump(self.interaction_graph, fp)

        with open(os.path.join(obnl_folder, self.RUN_JSON_FILE), 'w') as fp:
            json.dump({}, fp)  # TODO: generate and pass real run.json instead of empty dict

        client.containers.run(
            'integrcity/orchestrator',
            name='ict-orch',
            volumes={os.path.abspath(obnl_folder): {'bind': '/home/ictuser/work', 'mode': 'rw'}},
            command='{} {} {}'.format(self.HOST, self.SCE_JSON_FILE, self.RUN_JSON_FILE),
            detach=True,
            auto_remove=True)

        return client.containers.get('ict-orch').logs(stream=True)

    def deploy_nodes(self, client=None):
        """Deploy and run simulation nodes containers"""
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
