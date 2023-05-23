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
    def validate_JSON(self, json_path : Path, json_dict : dict):
        with open(json_path) as json_file:
            try:
                json_dict = json.load(json_file)
                return json_dict
            except ValueError as e:
                raise InputControlFailed(str(e))

class JSONConverter:
    """Class converts JSON format files into XML and YAML files.

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
        xml = xmltodict.unparse(self.JSON_file)
        return xml

    def convert_to_yaml(self):
        yml = yaml.dump(self.JSON_file)
        return yml





