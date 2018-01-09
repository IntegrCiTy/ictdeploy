import pytest

import os
import shutil
import docker

from deployict.deployment import SimNodesCreator as Sim

client = docker.from_env()
