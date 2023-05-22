#!/bin/python

import argparse
from pathlib import Path
from input_control import InputControl, InputControlFailed

class FileParser:
    __infile : Path
    __outfile : Path

    def __init__(self):
        self.__infile = Path()
        self.__outfile = Path()

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

        args = parser.parse_args()
        self.input_control(args.infile[0], args.outfile[0])

    def input_control(self, inarg, outarg):
        try:
            # try to validate the input
            ctrl = InputControl(inarg, outarg)

            # if successful, assign to class attributes
            self.infile = ctrl.infile
            self.outfile = ctrl.outfile

        except InputControlFailed as e:
            print(e)

if __name__ == '__main__':
    parser = FileParser()
    parser.parse_args()
