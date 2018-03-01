import logging
import json
from docopt import docopt

from obnl.core.impl.server import Scheduler

# This doc is used by docopt to make the server callable by command line and gather easily all the given parameters
doc = """>>> IntegrCiTy obnl command <<<

Usage:
	server.py (<host> <graph> <schedule>)
	server.py -h | --help
	server.py --version

Options
	-h --help   show this
	--version   show version

"""

if __name__ == "__main__":
    args = docopt(doc, version='0.0.1')

    Scheduler.activate_console_logging(logging.DEBUG)

    with open(args["<graph>"]) as json_data:
        graph_data = json.load(json_data)

    with open(args["<schedule>"]) as json_data:
        schedule_data = json.load(json_data)

    c = Scheduler(
        host=args["<host>"],
        vhost='obnl_vhost',
        username='obnl',
        password='obnl',
        config_file='config_file.json',
        simu_data=graph_data,
        schedule_data=schedule_data,
        log_level=logging.DEBUG)

    c.start()
