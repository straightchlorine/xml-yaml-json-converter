#!/bin/python

import yaml

import json
import xmltodict

from input_control import InputControlFailed
from pathlib import Path

class YAMLSyntaxCheck:
    """Class checks the syntax of given file.

    In the constructor it receives the YAML type file after that
    it verifies if the syntax is correct, if not throws InputControlFailed
    exception.

    """
    @staticmethod
    def validate_XML(yaml_path : Path):
        try:
            return yaml.safe_load(yaml_path.read_text())
        except yaml.YAMLError as e:
            raise InputControlFailed(str(e))

class YAMLConverter:
    """Class converts YAML files into JSON and XML files.

    Args:

        __XML_file (dict)  : dictionary containing the parsed YAML file
    """

    pass
