#!/bin/python

import argparse

from pathlib import Path

from markupconverter.parsing.input_control import InputControl
from markupconverter.parsing.input_exception import InputControlFailed

class FileParser:
    """Receives arguments passed to the script.

    Class users argparse module in order to get the arguments given
    by the user, after that it uses InputControl class to check
    if given data is valid.

    Args:
        __infile (Path)     : input file (to be converted)
        __outfile (Path)    : output file (converted)

    """
    __infile : Path
    __outfile : Path
    __parsed_dict : dict

    def __init__(self):
        self.__infile = Path()
        self.__outfile = Path()
        self.__parsed_dict = {}
        args = self.parse_args()

        # input control
        try:
            self.input_control(args.infile[0], args.outfile[0])
        except InputControlFailed as e:
            raise e

    @property
    def parsed_dict(self):
        return self.__parsed_dict

    @parsed_dict.setter
    def parsed_dict(self, dict):
        self.__parsed_dict = dict

    @property
    def infile(self):
        return self.__infile

    @infile.setter
    def infile(self, infile):
        self.__infile = infile

    @property
    def outfile(self):
        return self.__outfile

    @outfile.setter
    def outfile(self, outfile):
        self.__outfile = outfile

    def parse_args(self):
        parser = argparse.ArgumentParser(description='XML, JSON, YAML converter')

        parser.add_argument('infile', nargs=1, help='input file')
        parser.add_argument('outfile', nargs=1, help='converted file')

        # parsing the arguments
        return parser.parse_args()

    def input_control(self, inarg, outarg):
        try:
            # try to validate the input
            ctrl = InputControl(inarg, outarg)

            # if successful, assign to class attributes
            self.infile = ctrl.infile
            self.outfile = ctrl.outfile
            self.parsed_dict = ctrl.parsed_data
        except InputControlFailed as e:
            raise e

if __name__ == '__main__':
    parser = FileParser()
    parser.parse_args()
