# IntegrCiTy co-simulation deployment API

This package has been made to help in the deployment of a co-simulation using OBNL (url) as orchestrator.
It allows you to create simulation nodes, links, steps and running sequences.
The description for creating wrappers with your tools can be found here (url) as well as examples.
A full working demonstration of this package can be found here (url).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Python >= 3.5 (https://www.python.org/downloads/)
Docker Community-edition (https://www.docker.com/community-edition)
```

### Installing

A step by step series of examples that tell you have to get a development env running

Install git (if not already done) (More info on [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git))

If you’re on a Debian-based distribution like Ubuntu, try apt-get:

```
$ sudo apt-get install git-all
```

Install virtualenv (if not already done) (More info on [virtualenv](https://virtualenv.pypa.io/en/stable/installation/))

```
$ pip install virtualenv
```

Create a Python 3.5 virtual env

```
$ virtualenv -p python3 ict
```

Activate the created virtual env (ict)

```
$ source link/to/ict/bin/activate
```

Install dependencies

```
$ pip install -r requirements.txt
```

Install ictdeploy (in the ictdeploy folder)

```
$ python setup.py install
```

A full scale demo with real data and complex models will soon be available.

## Running the tests

Pytest (https://docs.pytest.org/en/latest/) is used in this project.
To run tests just run `pytest` with command line in the dedicated environment in the root forlder of this package.

### Break down into end to end tests

`test_creation.py` gathers the tests for the creation of the simulation graph (meta-models, models, nodes, links, ...).

```
pytest tests/test_creation.py
```

`test_command.py` gathers the tests for the execution of commands by wrappers inside Docker containers.
```
pytest tests/test_command.py
```

`test_deployment.py` gathers the tests for the deployment of all different nodes.
```
pytest tests/test_deployment.py
```

## Built With

* [Docker-SDK](http://docker-py.readthedocs.io/en/stable/) - python interface for the Docker Engine API
* [Networkx](https://networkx.github.io/) - manipulation of graph and network
* [Pandas](https://pandas.pydata.org/) - data structures and data analysis tools
* [OBNL](https://github.com/IntegrCiTy/obnl) - co-simulation orchestrator

## Authors

* **Pablo Puerto** - *Initial work*

## License

You should have received a copy of the Apache License Version 2.0 along with this program.
If not, see http://www.apache.org/licenses/LICENSE-2.0.

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc

