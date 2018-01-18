import docker
import json
import os
import shutil


class SimNodesCreator:
    CLIENT = docker.from_env()
    TMP_FOLDER = "TMP_FOLDER"
    INIT_VALUES_FILE = 'init_values.json'
    HOST = "172.17.01"

    def __init__(self):
        pass

    def _create_init_values_file(self, node_folder, init_values):
        init_json = os.path.join(node_folder, self.INIT_VALUES_FILE)
        with open(init_json, 'w') as outfile:
            json.dump(init_values, outfile)

    def create_volume(self, node_name, init_values, *files):
        node_folder = os.path.join(self.TMP_FOLDER, node_name)
        os.makedirs(node_folder)

        for file in files:
            shutil.copyfile(file, os.path.join(node_folder, os.path.basename(file)))

        self._create_init_values_file(node_folder, init_values)

        return node_folder

    def deploy_node(self, node_name, image, node_folder, wrapper, command=None, client=None):
        if client is None:
            client = self.CLIENT

        if command is None:
            command = []

        command = [os.path.basename(wrapper), self.HOST, node_name, self.INIT_VALUES_FILE, *command]

        client.containers.run(
            image=image,
            name=node_name,
            volumes={os.path.abspath(node_folder): {"bind": "/home/project", "mode": "rw"}},
            command=command,
            detach=True,
            auto_remove=True
        )

        return client.containers.get(node_name).logs(stream=True)
