import ctff_functions
import os


def config_collect(path):
    cfg_files = []
    base_folder_directories = os.listdir(path)

    for folder in base_folder_directories:
        folder = os.path.join(path, folder)
        if os.path.isdir(folder):
            parsed_config = ctff_functions.config_parse(folder)
            if parsed_config != 0:
                cfg_files.append(parsed_config)
    return cfg_files
