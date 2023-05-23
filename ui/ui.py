#!/bin/python

from pathlib import Path

from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QFileDialog, QLineEdit
from markupconverter.parsing.input_control import InputControl
from markupconverter.parsing.input_exception import InputControlFailed
from markupconverter.parsing.output_generator import GenerateOutput

class Converter(QWidget):
    __input : Path
    __output_dir : Path
    __output_no_suffix : str = ""
    __output_name : str = ""
    __output : Path

    @property
    def input(self):
        return self.__input

    @input.setter
    def input(self, path):
        self.__input = path

    @property
    def output(self):
        return self.__output

    @output.setter
    def output(self, path):
        self.__output = path

    @property
    def output_dir(self):
        return self.__output_dir

    @output_dir.setter
    def output_dir(self, path):
        self.__output_dir = path

    @property
    def output_name(self):
        return self.__output_name

    @output_name.setter
    def output_name(self, str):
        self.__output_name = str

    @property
    def output_no_suffix(self):
        return self.__output_no_suffix

    @output_no_suffix.setter
    def output_no_suffix(self, str):
        self.__output_no_suffix = str

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.input_file_button = QPushButton('Choose file you wish to convert.')
        self.input_file_button.clicked.connect(self.chooseInputFile)
        
        self.label = QLabel('Name of output file (extension is optional):')
        self.output_file_name = QLineEdit()
        self.output_file_name.returnPressed.connect(self.getOutputFileName)

        self.output_file_button = QPushButton('Choose the directory, where you wish to save converted file to.')
        self.output_file_button.clicked.connect(self.chooseOutputDir)

        self.convert_to_JSON = QPushButton('to JSON')
        self.convert_to_JSON.setEnabled(False)
        self.convert_to_JSON.clicked.connect(self.convertToJSON)

        self.convert_to_XML = QPushButton('to XML')
        self.convert_to_XML.setEnabled(False)
        self.convert_to_XML.clicked.connect(self.convertToXML)

        self.convert_to_YAML = QPushButton('to YAML')
        self.convert_to_YAML.setEnabled(False)
        self.convert_to_YAML.clicked.connect(self.convertToYAML)

        layout.addWidget(self.input_file_button)
        layout.addWidget(self.label)
        layout.addWidget(self.output_file_name)
        layout.addWidget(self.output_file_button)
        layout.addWidget(self.convert_to_JSON)
        layout.addWidget(self.convert_to_XML)
        layout.addWidget(self.convert_to_YAML)

        self.setLayout(layout)

    def convertToJSON(self):
        if self.output_no_suffix != '':
            self.output_name = self.output_no_suffix + '.json'
        self.output = self.output_dir / self.output_name

        try:
            inputControl = InputControl(self.input, self.output)
            print(self.input)
            print(self.output)
            GenerateOutput(self.input.suffix, self.output, inputControl.parsed_data)
        except InputControlFailed as e:
            self.convert_to_JSON.setStyleSheet('background-color: red; color: white;')
            self.convert_to_JSON.setText(str(e))

    def convertToXML(self):
        if self.output_no_suffix != '':
            self.output_name = self.output_no_suffix + '.xml'
        self.output = self.output_dir / self.output_name

        try:
            inputControl = InputControl(self.input, self.output)
            GenerateOutput(self.input.suffix, self.output, inputControl.parsed_data)
        except InputControlFailed as e:
            self.convert_to_XML.setStyleSheet('background-color: red; color: white;')
            self.convert_to_XML.setText(str(e))

    def convertToYAML(self):
        if self.output_no_suffix != '':
            self.output_name = self.output_no_suffix + '.yml'
        self.output = self.output_dir / self.output_name

        try:
            inputControl = InputControl(self.input, self.output)
            GenerateOutput(self.input.suffix, self.output, inputControl.parsed_data)
        except InputControlFailed as e:
            self.convert_to_YAML.setStyleSheet('background-color: red; color: white;')
            self.convert_to_YAML.setText(str(e))


    def chooseInputFile(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(self, "Choose File", "", "Markup files (*.xml *.json *yml)", options=options)

        self.input = Path(file)
        self.input_file_button.setText(f'{self.input.name} has been chosen.')

    def chooseOutputDir(self):
        directory = QFileDialog.getExistingDirectory(self, "Open Directory",
                                       "/home",
                                       QFileDialog.ShowDirsOnly
                                       | QFileDialog.DontResolveSymlinks)

        self.output_file_button.setText(f'{directory} has been chosen.')
        self.output_dir = Path(directory)
        self.process()

    def getOutputFileName(self):
        text = self.output_file_name.text()
        self.output_file_name.setPlaceholderText(text)
        self.output_file_name.setEnabled(False)
        self.checkIfSuffixGiven(text)

    def checkIfSuffixGiven(self, filename):
        if '.xml' in filename:
            self.output_name = filename
        elif '.json' in filename:
            self.output_name = filename
        elif '.yml' in filename:
            self.output_name = filename
        else:
            self.output_no_suffix = filename

    def suffixPresent(self):
        self.output = self.output_dir / self.output_name
        if self.output.suffix == '.xml':
            self.convert_to_XML.setEnabled(True)
        if self.output.suffix == '.json':
            self.convert_to_JSON.setEnabled(True)
        if self.output.suffix == '.yml':
            self.convert_to_YAML.setEnabled(True)

    def suffixAbsent(self):
        if self.input.suffix == '.xml':
            self.convert_to_XML.setEnabled(False)
            self.convert_to_JSON.setEnabled(True)
            self.convert_to_YAML.setEnabled(True)
        if self.input.suffix == '.json':
            self.convert_to_JSON.setEnabled(False)
            self.convert_to_XML.setEnabled(True)
            self.convert_to_YAML.setEnabled(True)
        if self.input.suffix == '.yml':
            self.convert_to_YAML.setEnabled(False)
            self.convert_to_XML.setEnabled(True)
            self.convert_to_JSON.setEnabled(True)

    def process(self):
        if self.output_name != '' and self.output_no_suffix == '':
            self.suffixPresent()
        elif self.output_name == '' and self.output_no_suffix != '':
            self.suffixAbsent()
