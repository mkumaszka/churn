# Sposob uzycia
# import Config.ConfigReader as config

import yaml
import os.path as path

config = dict()
root_folder = path.dirname(path.dirname(__file__))
config_path = path.join(root_folder, 'config.yaml')

with open(config_path, 'r') as stream:
    try:
        config = yaml.load(stream)
    except yaml.YAMLError as exc:
        print('Cannot find config file')
