import docker
import json
import os
import shutil

from ictdeploy.base_config import base_config
from ictdeploy.logs import logger


class SimNodesCreator:
    """
    Class for gathering methods allowing the deployment of simulation nodes
    """

    CLIENT = docker.from_env()
    """Default docker client"""

    TMP_FOLDER = "TMP_FOLDER"
    """Name of the temporary local folder"""

    INIT_VALUES_FILE = "init_values.json"
    """Default name for the initial values json file"""

    CONFIG_FILE = "config_file.json"
    """Name of the Protobuf configuration file"""

    HOST = "172.17.01"
    """Default host address for host of Redis and RabbitMQ"""

    BASE_CONFIG = base_config
    """Base configuration for Protobuf"""

    def __init__(self):
        pass

    def _create_init_values_file(self, node_folder, init_values):
        """
        Create the json file containing the initial values to be set in the node's model

        :param node_folder: the local path of the node's folder
        :param init_values: a dict mapping the initial values to the parameters names
        :return: nothing :)
        """
        init_json = os.path.join(node_folder, self.INIT_VALUES_FILE)
        with open(init_json, "w") as outfile:
            json.dump(init_values, outfile)

        logger.debug("Init values file created in {}".format(node_folder))

    def _create_config_file(self, node_name, node_folder):
        """
        Create the configuration file necessary for the RabbitMQ communication and the Protobuf protocol

        :param node_name: well... the name of the node
        :param node_folder: the local path of the node's folder
        :return: nothing :)
        """
        node_config = dict(self.BASE_CONFIG)
        node_config["name"] = node_name

        config_json = os.path.join(node_folder, self.CONFIG_FILE)
        with open(config_json, "w") as outfile:
            json.dump(node_config, outfile)

        logger.debug("Configuration file created in for {} in {}".format(node_name, node_folder))

    def create_volume(self, node_name, init_values, *files):
        """
        Create the local folder that will be "synchronized" with / mounted into the container

        :param node_name: well... the name of the node
        :param init_values: a dict mapping the initial values to the model's parameters
        :param files: bunch of files that need to be added to the container for running the wrapper
        :return: the local path of the node's folder
        """
        node_folder = os.path.join(self.TMP_FOLDER, node_name)
        os.makedirs(node_folder)

        for file in files:
            shutil.copyfile(file, os.path.join(node_folder, os.path.basename(file)))

        self._create_init_values_file(node_folder, init_values)
        self._create_config_file(node_name, node_folder)

        logger.debug("Volume created for {} in {}".format(node_name, node_folder))

        return node_folder

    def deploy_node(self, node_name, node, node_folder, client):
        """
        Deploy a simulation node, create and send command and mount the dedicated local volume into the container

        :param node_name: well... the name of the node
        :param node: a dict mapping all the necessary information to run the node (image, wrapper, etc.)
        :param node_folder: the local path of the node's folder
        :param client: the Docker client
        :return: a generator giving access to the node's logs
        """
        if client is None:
            client = self.CLIENT

        # Create specific command for input and output parameters
        param_i = ["--i={}".format(p) for p in node["to_set"]]
        param_o = ["--o={}".format(p) for p in node["to_get"]]

        # Build the command with the wrapper, the host, the name of the files with the initial values and the parameters
        full_command = [
            os.path.basename(node["wrapper"]),
            self.HOST,
            node_name,
            self.INIT_VALUES_FILE,
            *param_i,
            *param_o,
        ]

        # Add the "--first" option if the node is in the first group of the sequence
        if node["is_first"]:
            full_command.append("--first")

        # Add additional command
        if node["command"]:
            full_command.append("--cmd={}".format(node["command"]))

        if node["is_local"]:
            logger.info("The node {} needs to be deployed manually in the temporary node folder.".format(node_name))
            return " ".join(["python"] + full_command)

        else:
            # Run the container with the Docker API
            client.containers.run(
                image=node["image"],
                name=node_name,
                volumes={os.path.abspath(node_folder): {"bind": "/home/project", "mode": "rw"}},
                command=full_command,
                detach=True,
                auto_remove=True,
            )

            logger.info("The node {} is deployed.".format(node_name))

            return client.containers.get(node_name).logs(stream=True)
