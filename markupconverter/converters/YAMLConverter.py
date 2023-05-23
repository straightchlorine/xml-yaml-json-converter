#!/bin/python

import yaml

import json
import xmltodict

from markupconverter.parsing.input_control import InputControlFailed
from pathlib import Path

class YAMLSyntaxCheck:
    """Class checks the syntax of given file.

    In the constructor it receives the YAML type file after that
    it verifies if the syntax is correct, if not throws InputControlFailed
    exception.

    """
    @staticmethod
    def validate_yaml(yaml_path : Path):
        try:
            return yaml.safe_load(yaml_path.read_text())
        except yaml.YAMLError as e:
            raise InputControlFailed(str(e))

class YAMLConverter:
    """Class converts YAML files into JSON and XML files.

    Args:

        __YAML_file (dict)  : dictionary containing the parsed YAML file
    """

    __YAML_file : dict = {}

    @property
    def YAML_file(self):
        return self.__YAML_file

    @YAML_file.setter
    def YAML_file(self, YAML_dict):
        self.__YAML_file = YAML_dict

    def __init__(self, YAML_dict):
        self.YAML_file = YAML_dict

    def convert_to_json(self):
        return json.dumps(self.YAML_file, indent = 4)

    def convert_to_xml(self):
        return xmltodict.unparse(self.YAML_file, pretty = True)

# testing
if __name__ == "__main__":
    yamlconv = YAMLConverter(YAMLSyntaxCheck.validate_yaml(Path('../test_data/component.yml')))
    print(yamlconv.convert_to_json())
    print(yamlconv.convert_to_xml())
