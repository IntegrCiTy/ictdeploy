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

    def deploy_node(self, node_name, node, node_folder, client):
        if client is None:
            client = self.CLIENT

        param_i = ["--i={}".format(p) for p in node["to_set"]]
        param_o = ["--o={}".format(p) for p in node["to_get"]]

        full_command = [
            os.path.basename(node["wrapper"]),
            self.HOST, node_name,
            self.INIT_VALUES_FILE,
            *param_i,
            *param_o]

        if node["is_first"]:
            full_command.append("--first")

        if node["command"]:
            full_command.append("--cmd={}".format(node["command"]))

        client.containers.run(
            image=node["image"],
            name=node_name,
            volumes={os.path.abspath(node_folder): {"bind": "/home/project", "mode": "rw"}},
            command=full_command,
            detach=True,
            auto_remove=True
        )

        return client.containers.get(node_name).logs(stream=True)
