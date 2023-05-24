#!/bin/python

from markupconverter.parsing.input_exception import InputControlFailed
from markupconverter.parsing.output_generator import GenerateOutput
from markupconverter.parsing.parser import FileParser

from ui.ui import Converter

from PyQt5.QtWidgets import QApplication

import sys

class MarkupConverter:
    def __init__(self):
        try:
            parser = FileParser()
            print(f'Starting conversion of {parser.infile.name} to {parser.outfile.name}...')
            GenerateOutput(parser.infile.suffix, parser.outfile, parser.parsed_dict)
            print(f'{parser.infile.name} has been converted to {parser.outfile}')
        except InputControlFailed as e:
            print(e)

    @staticmethod
    def ui():
        app = QApplication(sys.argv)
        window = Converter()
        window.resize(855, 240)
        window.show()
        sys.exit(app.exec_())

# driver code
if __name__ == "__main__":
    #converter = MarkupConverter()
    MarkupConverter.ui()
