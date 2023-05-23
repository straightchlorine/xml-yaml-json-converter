#!/bin/python

from pathlib import Path

from markupconverter.converters.JSONConverter import JSONConverter
from markupconverter.converters.XMLConverter import XMLConverter
from markupconverter.converters.YAMLConverter import YAMLConverter

class GenerateOutput:
    def __init__(self, insuffix : str, outpath : Path, data : dict):
        with open(outpath, 'w') as output:
            if insuffix == '.json':
                if outpath.suffix == '.yml':
                    output.write(JSONConverter(data).convert_to_yaml())
                if outpath.suffix == '.xml':
                    output.write(JSONConverter(data).convert_to_xml())
            if insuffix == '.yml':
                if outpath.suffix == '.json':
                    output.write(YAMLConverter(data).convert_to_json())
                if outpath.suffix == '.xml':
                    output.write(YAMLConverter(data).convert_to_xml())
            if insuffix == '.xml':
                if outpath.suffix == '.yml':
                    output.write(XMLConverter(data).convert_to_yaml())
                if outpath.suffix == '.json':
                    output.write(XMLConverter(data).convert_to_json())

