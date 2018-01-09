import os
import shutil

from deployict.deployment import SimNodesCreator as Sim

tests_folder = "tests"
files_folder = "files_to_add"
wraps_folder = "wrappers"


def clean_tmp_folder(folder=Sim.TMP_FOLDER):
    if os.path.isdir(folder):
        shutil.rmtree(folder)


def clean_containers(containers=Sim.CLIENT.containers):
    containers.prune()

    for container in containers.list():
        container.kill()


def get_logs(logs):
    outputs = []
    while True:
        try:
            outputs.append(logs.__next__().decode("utf-8").rstrip())
        except StopIteration:
            break
    return outputs
