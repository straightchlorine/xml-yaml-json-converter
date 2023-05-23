#!/bin/python

import json

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
    """Class converts XML and YAML format files into JSON files.

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

    def convert_to_xml():
        pass

    def convert_to_yaml():
        pass





