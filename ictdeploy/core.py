from ictdeploy.deployment import SimNodesCreator
from ictdeploy.interactions import GraphCreator

import numpy as np

import time
import json
import os
import shutil

from ictdeploy.base_config import obnl_config


# TODO: set up a correct logger
# from ictdeploy.logs import my_logger


class Simulator(GraphCreator, SimNodesCreator):

    """
    Main class to import for co-simulation running, it gathers all the useful methods.
    """

    SCE_JSON_FILE = "interaction_graph.json"
    RUN_JSON_FILE = "sequences_and_steps.json"
    UNITS = {"seconds": 1, "minutes": 60, "hours": 3600}

    RABBITMQ_ADMIN_PASSWORD = "admin"
    RABBITMQ_OBNL_PASSWORD = "obnl"
    RABBITMQ_TOOL_PASSWORD = "tool"

    def __init__(self):
        super().__init__()

        self.sequence = []
        self.steps = []

    def _clean_all(self, client):
        """
        Delete the temporary folder and kill all the existing containers

        :param client: Docker client (default: from local environment)
        :return:
        """
        if os.path.isdir(self.TMP_FOLDER):
            shutil.rmtree(self.TMP_FOLDER)

        client.containers.prune()

        for container in client.containers.list():
            container.kill()

    def deploy_aux(self, client=None):
        """
        Deploy the Redis (results database) and the RabbitMQ (communication) containers

        :param client: Docker client (default: from local environment)
        :return: a dict containing the logs of the Redis and the RabbitMQ containers as generators
        """

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
            'ict-rabbitmq',
            name='ict-rab',
            ports={'5672/tcp': 5672},
            environment={
                'RABBITMQ_ADMIN_PASSWORD': self.RABBITMQ_ADMIN_PASSWORD,
                'RABBITMQ_OBNL_PASSWORD': self.RABBITMQ_OBNL_PASSWORD,
                'RABBITMQ_TOOL_PASSWORD': self.RABBITMQ_TOOL_PASSWORD,
            },
            detach=True,
            auto_remove=True)

        time.sleep(10)

        red_logs = client.containers.get("ict-red").logs(stream=True)
        rab_logs = client.containers.get("ict-rab").logs(stream=True)

        return {"ict-red": red_logs, "ict-rab": rab_logs}

    def deploy_orchestrator(self, simulation="demotest", client=None):
        """
        Deploy and configure the OBNL (orchestration) container

        :param client: Docker client (default: from local environment)
        :param simulation:
        :return: logs of the OBNL container as generator
        """
        if client is None:
            client = self.CLIENT

        obnl_folder = os.path.join(self.TMP_FOLDER, "obnl_folder")
        os.makedirs(obnl_folder)

        with open(os.path.join(obnl_folder, self.SCE_JSON_FILE), 'w') as fp:
            json.dump(self.interaction_graph, fp)

        with open(os.path.join(obnl_folder, self.RUN_JSON_FILE), 'w') as fp:
            json.dump({"steps": self.steps, "schedule": self.sequence, "simulation_name": simulation}, fp)

        with open(os.path.join(obnl_folder, self.CONFIG_FILE), 'w') as fp:
            json.dump(obnl_config, fp)

        shutil.copyfile("server.py", os.path.join(obnl_folder, "server.py"))

        client.containers.run(
            'ict-obnl',
            name='ict-orch',
            volumes={os.path.abspath(obnl_folder): {'bind': "/home/project", 'mode': 'rw'}},
            command='{} {} {}'.format(self.HOST, self.SCE_JSON_FILE, self.RUN_JSON_FILE),
            detach=True,
            auto_remove=True)

        return client.containers.get('ict-orch').logs(stream=True)

    def deploy_nodes(self, client=None):
        """
        Deploy and run the simulation nodes containers

        :param client: Docker client (default: from local environment)
        :return: a dict containing the logs of the nodes containers as generators
        """
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
        """
        Create a group for the simulation sequence verifying that none of the group's nodes are directly connected

        :param nodes: some nodes names
        :return: selected nodes names as a list
        """
        h = self._graph.subgraph(nodes)
        try:
            assert len(h.edges) == 0
        except AssertionError:
            for get_node, set_node, _ in h.edges:
                print("WARNING - A direct link exists from {} to {} !".format(get_node, set_node))
        return nodes

    def create_sequence(self, *groups):
        """
        Create the simulation's sequence

        :param groups: some groups as list of nodes (created by self.create_group)
        :return:
        """
        self.sequence = [g for g in groups]

    def create_steps(self, steps, unit="seconds"):
        """
        Create the simulation's steps

        :param steps: list of simulation time-steps to run
        :param unit: time unit of steps (default: seconds)
        :return:
        """
        steps = np.array(steps) * self.UNITS[unit]
        self.steps = steps.tolist()
