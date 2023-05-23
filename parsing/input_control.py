#!/bin/python

from pathlib import Path

class InputControlFailed(Exception):
    """Exception raised if validation in InputControl fails"""
    def __init__(self, message):
        super().__init__(message)

class InputControl:
    """Class responsible for input control.

    Class receives both arguments obtained by FileParser and
    checks whether requirements are fullfiled.

    First input:
        - must exist
        - must be of type .xml, .json or .yml
        - syntax must be verified

    Second input:
        - can exist
        - must be of type .xml, .json or .yml
    """
    __infile : Path
    """Contains input file."""

    __outfile : Path
    """Contains output file"""

    @property
    def infile(self):
        return self.__infile

    @infile.setter
    def args(self, infile):
        self.__infile = infile

    @property
    def outfile(self):
        return self.__outfile

    @outfile.setter
    def outfile(self, outfile):
        self.__outfile = outfile

    def __init__(self, infile, outfile):
        input_file = Path()
        output_file = Path()
        """Constructor

        Args:
            input_file (string)  : contains path of input file
            output_file (string) : contains path of output file

        """
        try:
            input_file = Path(infile)
            output_file = Path(outfile)
            input_file.absolute()
            output_file.absolute()

            # checking if the first file exists
            self.verify_existence(input_file)

            # checking whether extensions work
            self.verify_extension(input_file)
            self.verify_extension(output_file)

            # checking if the syntax is correct
            self.check_syntax(input_file)

            self.__infile = input_file
            self.__outfile = output_file
        except InputControlFailed as e:
            raise e

    def verify_existence(self, path : Path):
        """Checks if given file exists

        Returns:
            bool: true if file exists

        Raises:
            InputControlFailed: if requirement is not met

        """
        if path.is_file() and path.exists():
            return True
        else:
            raise InputControlFailed(f'{path} does not exist.')

    def verify_extension(self, path : Path):
        """Checks extension of the file.

        Returns:
            bool: true if extension is either .xml, .yml or .json

        Raises:
            InputControlFailed: if requirement is not met

        """
        if path.suffix in ['.xml', '.yml', '.json']:
            return True
        else:
            raise InputControlFailed(f'{path} extension is unsupported.')

    def check_syntax(self, infile):
        pass

