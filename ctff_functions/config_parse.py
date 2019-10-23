# config_parse.py
import os
from configparser import ConfigParser

config_file_name = 'info.cfg'


class CtffModuleConfig(object):
    prettyName = ''
    setupFile = ''

    def __init__(self, prettyname, setupfile):
        self.prettyName = prettyname
        self.setupFile = setupfile


def config_parse(folder):
    if os.path.join(folder, config_file_name):
        config_file = os.path.join(folder, config_file_name)
    else:
        exit(1)
    config = ConfigParser()
    config.read(config_file)
    module_identity = config["module-identity"]
    module_pretty_name = module_identity["pretty-name"]
    module_options = config["module-options"]
    module_run_script = module_options["run-script"]
    module_run_script = os.path.join(folder, module_run_script)
    module_configuration = CtffModuleConfig(module_pretty_name, module_run_script)
    return module_configuration
