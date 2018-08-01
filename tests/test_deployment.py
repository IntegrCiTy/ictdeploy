import os
import docker

from ictdeploy import Simulator as Sim

from tests.common import clean_tmp_folder, clean_containers, get_logs
from tests.fixtures_test import fix_create, fix_deploy


# def test_needed_files_are_in_the_obnl_folder_before_simulation(fix_deploy):
#     sim, _, _, _ = fix_deploy
#     files = {"interaction_graph.json", "sequences_and_steps.json", "config_file.json"}
#     assert set(os.listdir(os.path.join(sim.deploy.TMP_FOLDER, "obnl_folder"))) == files


def test_obnl_image_contains_server():
    sim = Sim()
    client = docker.client.from_env()
    logs = client.containers.run(
        sim.OBNL_DOCKER_IMAGE,
        command="-h",
        volumes={os.path.abspath(os.path.join("tests", "files_to_add")): {"bind": "/home/project", "mode": "rw"}},
        auto_remove=True
    )
    assert "server.py (<host> <graph> <schedule>)" in logs.decode("utf-8")


def test_rabbitmq_and_redis_are_running(fix_deploy):
    sim, _, _, _ = fix_deploy
    assert sim.deploy.CLIENT.containers.get("ict_rab").status == "running"
    assert sim.deploy.CLIENT.containers.get("ict_red").status == "running"

# TODO: test activity.log in all nodes folder after deployment
# TODO: test deployment.log and server.py in obnl's folder after deployment


def test_run_simulation_method(fix_create):
    sim = fix_create
    logs = sim.run_simulation()
    full_orch_logs = sim.get_logs(logs["orc"])
    for l in full_orch_logs:
        print("ORCH LOGS -> {}".format(l))
    assert len([l for l in full_orch_logs if "Simulation finished." in l]) == 1


def test_simulation_run_until_the_end(fix_deploy):
    sim, logs_aux, logs_orc, logs = fix_deploy
    assert len([l for l in get_logs(logs_orc) if "Simulation finished." in l]) == 1


def teardown_function():
    # clean_tmp_folder()
    clean_containers()
