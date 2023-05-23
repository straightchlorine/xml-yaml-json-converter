#!/bin/python

import xmltodict

import json
import yaml

from input_control import InputControlFailed
from pathlib import Path

class XMLSyntaxCheck:
    """Class checks the syntax of given file.

    In the constructor it receives the XML type file after that
    it verifies if the syntax is correct, if not throws InputControlFailed
    exception.

    """
    @staticmethod
    def validate_XML(xml_path : Path):
        try:
            return xmltodict.parse(xml_path.read_text())
        except xmltodict.ParsingInterrupted as e:
            raise InputControlFailed(str(e))

class XMLConverter:
    """Class converts XML files into JSON and YAML files.

    Args:

        __XML_file (dict)  : dictionary containing the parsed and valid XML file
    """
    __XML_file : dict = {}

    @property
    def XML_file(self):
        return self.__XML_file

    @XML_file.setter
    def XML_file(self, XML_dict):
        self.__XML_file = XML_dict

    def __init__(self, XML_dict):
        self.XML_file = XML_dict

    def convert_to_json(self):
        json_str = json.dumps(self.XML_file, indent = 4)
        return json_str

    def convert_to_yaml(self):
        yml = yaml.dump(self.XML_file)
        return yml
