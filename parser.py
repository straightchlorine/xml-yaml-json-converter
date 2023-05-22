#!/bin/python

import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='XML, JSON, YAML converter')

    parser.add_argument('infile', nargs=1, help='input file')
    parser.add_argument('outfile', nargs=1, help='converted file')

    files = parser.parse_args()

if __name__ == '__main__':
     parse_args()

