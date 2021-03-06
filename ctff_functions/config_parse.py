import os
from configparser import ConfigParser

config_file_name = 'info.cfg'


class CtffModuleConfig(object):
    moduleType = ''
    modulePrettyName = ''
    moduleAction = ''
    modulePath = ''

    def __init__(self, moduletype, moduleprettyname, moduleaction, modulepath):
        self.moduleType = moduletype
        self.modulePrettyName = moduleprettyname
        self.moduleAction = moduleaction
        self.modulePath = modulepath


def config_parse(folder):
    if os.path.exists(os.path.join(folder, config_file_name)):
        config_file = os.path.join(folder, config_file_name)
    else:
        return 0
    config = ConfigParser()
    try:
        config.read(config_file)
    except Exception as e:
        print(e)
    module_info = config["module-info"]
    module_type = module_info["module-type"]
    try:
        module_prettyname = module_info["pretty-name"]
    except Exception as e:
        module_prettyname = 'No PrettyName'

    try:
        module_action = module_info["action"]
    except Exception as e:
        module_action = ""

    module_configuration = CtffModuleConfig(module_type, module_prettyname, module_action, folder)
    return module_configuration
