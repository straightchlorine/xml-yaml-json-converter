#!/bin/python

from markupconverter.parsing.input_exception import InputControlFailed
from markupconverter.parsing.output_generator import GenerateOutput
from markupconverter.parsing.parser import FileParser

class MarkupConverter:
    def __init__(self):
        try:
            parser = FileParser()
            print(f'Starting conversion of {parser.infile.name} to {parser.outfile.name}...')
            GenerateOutput(parser.infile.suffix, parser.outfile, parser.parsed_dict)
            print(f'{parser.infile.name} has been converted to {parser.outfile}')
        except InputControlFailed as e:
            print(e)

# driver code
if __name__ == "__main__":
    converter = MarkupConverter()
