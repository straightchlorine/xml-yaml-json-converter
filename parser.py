#!/bin/python

import argparse

class FileParser:
    __args : argparse.Namespace

    def __init__(self):
        self.__args = argparse.Namespace()

    @property
    def args(self):
        return self.__args

    @args.setter
    def args(self, args):
        self.__args = args

    def parse_args(self):
        parser = argparse.ArgumentParser(description='XML, JSON, YAML converter')

        parser.add_argument('infile', nargs=1, help='input file')
        parser.add_argument('outfile', nargs=1, help='converted file')

        self.args = parser.parse_args()

if __name__ == '__main__':
    parser = FileParser()
    parser.parse_args()
    print(parser.args)

