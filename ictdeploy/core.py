from ictdeploy.deployment import SimNodesCreator
from ictdeploy.interactions import GraphCreator

import numpy as np

import time
import json
import os
import shutil


# TODO: set up correctly logger
# from ictdeploy.logs import my_logger


class Simulator(GraphCreator, SimNodesCreator):
    SCE_JSON_FILE = "interaction_graph.json"
    RUN_JSON_FILE = "sequences_and_steps.json"
    UNITS = {"seconds": 1, "minutes": 60, "hours": 3600}

    def __init__(self):
        super().__init__()

        self.sequence = []
        self.steps = []

    def _clean_all(self, client):
        if os.path.isdir(self.TMP_FOLDER):
            shutil.rmtree(self.TMP_FOLDER)

        client.containers.prune()

        for container in client.containers.list():
            container.kill()

    def deploy_aux(self, client=None):

        """Deploy Redis (results database) and RabbitMQ (communication) containers"""
        if client is None:
            client = self.CLIENT

        self._clean_all(client)

        client.containers.run(
            'redis:alpine',
            name='ict-red',
            ports={'6379/tcp': 6379},
            detach=True,
            auto_remove=True)

        client.containers.run(
            'integrcity/rabbitmq',
            # "rabbitmq:alpine",
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
            json.dump({"steps": self.steps, "schedule": self.sequence}, fp)

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

        nodes = self.nodes

        for node_name, node in nodes.iterrows():

            node_folder = self.create_volume(
                node_name,
                node["init_values"],
                node["wrapper"],
                *node["files"]
            )

            logs[node_name] = self.deploy_node(
                node_name=node_name,
                node=node,
                node_folder=node_folder,
                client=client
            )
        return logs

    def create_group(self, *nodes):
        """Create group for simulation sequence verifying that none of the group's nodes are directly connected"""
        h = self._graph.subgraph(nodes)
        try:
            assert len(h.edges) == 0
        except AssertionError:
            for get_node, set_node, _ in h.edges:
                print("WARNING - A direct link exists from {} to {} !".format(get_node, set_node))
        return nodes

    def create_sequence(self, *groups):
        """Create simulation sequences"""
        self.sequence = [g for g in groups]

    def create_steps(self, steps, unit="seconds"):
        steps = np.array(steps) * self.UNITS[unit]
        self.steps = steps.tolist()
