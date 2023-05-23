#!/bin/python

from pathlib import Path

from markupconverter.parsing.input_exception import InputControlFailed

from markupconverter.converters.JSONConverter import JSONSyntaxCheck
from markupconverter.converters.XMLConverter import XMLSyntaxCheck
from markupconverter.converters.YAMLConverter import YAMLSyntaxCheck


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
    """Contains output file."""

    __inextension : str
    """Extension of input file."""

    __outextension : str
    """Extension of output file."""

    __parsed_data : dict
    """Contains the dictionary made out of markup file."""

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

    @property
    def inextension(self):
        return self.__inextension

    @inextension.setter
    def inextension(self, inextension):
        self.__inextension = inextension

    @property
    def outextension(self):
        return self.__outextension

    @outextension.setter
    def outextension(self, outextension):
        self.__outextension = outextension

    @property
    def parsed_data(self):
        return self.__parsed_data

    @parsed_data.setter
    def parsed_data(self, parsed_dict):
        self.__parsed_data = parsed_dict

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

            self.__infile = input_file
            self.__outfile = output_file

            self.inextension = self.infile.suffix
            self.outextension = self.outfile.suffix

            # checking if the syntax is correct
            self.check_syntax(input_file)
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
        try:
            data_object = {}
            if self.inextension == '.json':
                data_object = JSONSyntaxCheck.validate_JSON(infile)
            if self.inextension == '.xml':
                data_object = XMLSyntaxCheck.validate_XML(infile)
            if self.inextension == '.yml':
                data_object = YAMLSyntaxCheck.validate_YAML(infile)
            self.parsed_data = data_object
        except InputControlFailed as e:
            raise InputControlFailed(f'{infile} file syntax is invalid \n {str(e)}.')

if __name__ == "__main__":
    incontrol = InputControl('./test_data/component.xml', 'component.yml' )
    print(incontrol.parsed_data)
