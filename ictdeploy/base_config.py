"""
This file define basic configuration for RabbitMQ and Protobuf communication
for the simulation nodes and the orchestrator nodes.
"""

base_config = {
    "name": "",
    "queues": {
        "obnl.simulation.node.": "on_simulation",
        "obnl.local.node.": "on_local",
        "obnl.data.node.": "on_data",
    },
    "exchanges": {
        "obnl.local.node.": {"binding": ["obnl.local.node."]},
        "obnl.simulation.node.": {"binding": ["obnl.simulation.node.scheduler"]},
    },
}

obnl_config = {
    "name": "scheduler",
    "queues": {"obnl.simulation.node.": "on_simulation"},
    "exchanges": {"obnl.simulation.node.": {"binding": []}},
}
