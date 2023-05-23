#!/bin/python

import xmltodict

import json
import yaml

from ..parsing.input_control import InputControlFailed
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
    """Class converts XML format files into JSON and YAML files.

    Args:

        __XML_file (dict)  : dictionary containing the parsed XML file
                                not None only if valid
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
        return json.dumps(self.XML_file, indent = 4)

    def convert_to_yaml(self):
        return yaml.dump(self.XML_file)

# testing driver code
if __name__ == "__main__":
    xmlconv = XMLConverter(XMLSyntaxCheck.validate_XML(Path('component.xml')))
    jsonfile = open('component.json', 'w')
    jsonfile.write(xmlconv.convert_to_json())
    jsonfile.close()

    ymlfile = open('component.yml', 'w')
    ymlfile.write(xmlconv.convert_to_yaml())
    ymlfile.close()
