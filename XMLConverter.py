#!/bin/python

import json

import xmltodict
import yaml


from input_control import InputControlFailed
from pathlib import Path

class XMLSyntaxCheck:
    """Class checks the syntax of given file.

    In the constructor it receives the XML type file after that
    it verifies if the syntax is correct, if not throws InputControlFailed
    exception.

    """
    def validate_XML(self, xml_path : Path, xml_dict : dict):
        with open(xml_path) as xml_file:
            try:
                xml_dict = xmltodict.parse(xml_path.read_text())
                return xml_dict
            except xmltodict.ParsingInterrupted as e:
                raise InputControlFailed(str(e))

class XMLConverter:
    """Class converts XML and YAML format files into XML files.

    Args:

        __XML_file (dict)  : dictionary containing the parsed JSON file
                                not None only if valid
    """
    pass
