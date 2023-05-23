#!/bin/python

import json

import xmltodict
import yaml


from input_control import InputControlFailed
from pathlib import Path

class JSONSyntaxCheck:
    """Class checks the syntax of given file.

    In the constructor it receives the JSON type file after that
    it verifies if the syntax is correct, if not throws InputControlFailed
    exception.

    """
    @staticmethod
    def validate_JSON(json_path : Path):
        with open(json_path) as json_file:
            try:
                return json.load(json_file)
            except ValueError as e:
                raise InputControlFailed(str(e))

class JSONConverter:
    """Class converts JSON files into XML and YAML files.

    Args:

        __JSON_file (dict)  : dictionary containing the parsed JSON file
                                not None only if valid
    """
    __JSON_file : dict = {}

    @property
    def JSON_file(self):
        return self.__JSON_file

    @JSON_file.setter
    def JSON_file(self, JSON_dict):
        self.__JSON_file = JSON_dict

    def __init__(self, JSON_dict):
        self.JSON_file = JSON_dict

    def convert_to_xml(self):
        return xmltodict.unparse(self.JSON_file, pretty = True)

    def convert_to_yaml(self):
        return yaml.dump(self.JSON_file)

# testing
if __name__ == "__main__":
    jsonconv = JSONConverter(JSONSyntaxCheck.validate_JSON(Path('component.json')))

    print(jsonconv.convert_to_xml())
    print(jsonconv.convert_to_yaml())
