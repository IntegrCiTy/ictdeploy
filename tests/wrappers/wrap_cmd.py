from docopt import docopt


doc = """>>> IntegrCiTy wrapper command <<<

Usage:
	wrapper.py (<host> <name> <init>) [--i=TO_SET... --o=TO_GET... --first --cmd=CMD]
	wrapper.py -h | --help
	wrapper.py --version

Options
	-h --help   show this
	--version   show version
	--i         parameters to set
	--o         parameters to get
	--first     node in sequence's first group
	--cmd       optional list of commands to run wrapper

"""

if __name__ == "__main__":
    arguments = docopt(doc, version="0.0.1")
    print(arguments)
