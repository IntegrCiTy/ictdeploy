import os
import shutil

from ictdeploy.deployment import SimNodesCreator as Sim

tests_folder = "tests"
files_folder = "files_to_add"
wraps_folder = "wrappers"


def clean_tmp_folder(folder=Sim.TMP_FOLDER):
    """
    Delete temporary folder that have been used to gather the folders mounted inside the containers

    :param folder:
    :return: nothing :)
    """
    if os.path.isdir(folder):
        shutil.rmtree(folder)


def clean_containers(containers=Sim.CLIENT.containers):
    """
    Stop, kill and remove all the "ict" containers

    :param containers:
    :return:
    """
    containers.prune()

    for container in containers.list():
        if "ict" in container.name:
            try:
                container.stop()
            except:
                pass

    for container in containers.list():
        if "ict" in container.name:
            try:
                container.kill()
            except:
                pass


def get_logs(logs):
    """
    Allow to transform generator of logs to readable list of str

    :param logs: generator of logs from an other process
    :return: a list of values given by the logs generator until "StopIteration"
    """
    outputs = []
    while True:
        try:
            outputs.append(logs.__next__().decode("utf-8").rstrip())
        except StopIteration:
            break
    return outputs
