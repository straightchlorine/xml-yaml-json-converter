#!/bin/python

from pathlib import Path


import threading
from PyQt5.QtCore import QMutex, QObject, QThread, QWaitCondition, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QLabel, QMainWindow, QWidget, QPushButton, QVBoxLayout, QFileDialog, QLineEdit

from markupconverter.parsing.input_control import InputControl
from markupconverter.parsing.input_exception import InputControlFailed
from markupconverter.parsing.output_generator import GenerateOutput


class Emitter(QObject):
    input = pyqtSignal(Path)
    output_dir = pyqtSignal(Path)
    output_no_suffix = pyqtSignal(str)
    output_name = pyqtSignal(str)
    output = pyqtSignal(Path)

    def sendInput(self, input):
        self.input.emit(input)

    def sendOutput_dir(self, output_dir):
        self.output_dir.emit(output_dir)

    def sendOutput_no_suffix(self, output_no_suffix):
        self.output_no_suffix.emit(output_no_suffix)

    def sendOutput_name(self, output_name):
        self.output_name.emit(output_name)

    def sendOutput(self, output):
        self.output.emit(output)

class Receiver(QObject):
    input : Path
    output_dir : Path
    output_no_suffix : str
    output_name : str
    output : Path

    def __init__(self):
        super().__init__()
        self.input = Path()
        self.output_dir = Path()
        self.output_no_suffix = ''
        self.output_name = ''
        self.output = Path()

    def handleInput(self, input):
        self.input = input

    def handleOutput_dir(self, output_dir):
        self.output_dir = output_dir

    def handleOutput_no_suffix(self, output_no_suffix):
        self.output_no_suffix = output_no_suffix

    def handleOutput_name(self, output_name):
        self.output_name = output_name

    def handleOutput(self, output):
        self.output = output

    def clearCache(self):
        self.input = Path()
        self.output_dir = Path()
        self.output_no_suffix = ''
        self.output_name = ''
        self.output = Path()

class Converter(QWidget):

    def __init__(self):
        super().__init__()

        self.emitter = Emitter()
        self.receiver = Receiver()

        # two separate threads responsible for loading the file
        # as well as converting it
        self.loaderThread = None
        self.converterThread = None
        self.outputThread = None

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.comm = QLabel('Please fill following parameters in order (top to down).')

        self.input_file_button = QPushButton('Choose file you wish to convert.')
        self.input_file_button.clicked.connect(self.chooseInputFile)

        self.label = QLabel('Name of output file (extension is optional), confirm with Enter:')
        self.output_file_name = QLineEdit()
        self.output_file_name.returnPressed.connect(self.getOutputFileName)

        self.output_file_button = QPushButton('Choose the directory, where you wish to save converted file to.')
        self.output_file_button.clicked.connect(self.outputDir)

        self.convert_to_JSON = QPushButton('to JSON')
        self.convert_to_JSON.setEnabled(False)
        self.convert_to_JSON.clicked.connect(self.JSONConversion)

        self.convert_to_XML = QPushButton('to XML')
        self.convert_to_XML.setEnabled(False)
        self.convert_to_XML.clicked.connect(self.XMLConversion)

        self.convert_to_YAML = QPushButton('to YAML')
        self.convert_to_YAML.setEnabled(False)
        self.convert_to_YAML.clicked.connect(self.YAMLConversion)

        self.new_file_button = QPushButton('New file')
        self.new_file_button.clicked.connect(self.newFile)

        # signals
        self.emitter.input.connect(self.receiver.handleInput)
        self.emitter.output_dir.connect(self.receiver.handleOutput_dir)
        self.emitter.output_no_suffix.connect(self.receiver.handleOutput_no_suffix)
        self.emitter.output_name.connect(self.receiver.handleOutput_name)
        self.emitter.output.connect(self.receiver.handleOutput)

        layout.addWidget(self.comm)
        layout.addWidget(self.input_file_button)
        layout.addWidget(self.label)
        layout.addWidget(self.output_file_name)
        layout.addWidget(self.output_file_button)
        layout.addWidget(self.convert_to_JSON)
        layout.addWidget(self.convert_to_XML)
        layout.addWidget(self.convert_to_YAML)
        layout.addWidget(self.new_file_button)

        self.setLayout(layout)

    def newFile(self):
        # clearing the receiver
        self.receiver.clearCache()

        # file dialogs
        self.input_file_button.setText('Choose file you wish to convert.')
        self.output_file_button.setText('Choose the directory, where you wish to save converted file to.')

        # line dialog
        self.output_file_name.clear()
        self.output_file_name.setEnabled(True)

        # converters
        self.convert_to_JSON.setEnabled(False)
        self.convert_to_XML.setEnabled(False)
        self.convert_to_YAML.setEnabled(False)

    def chooseInputFile(self):
        """Opens File dialog and allows to chose only applciable files."""
        options = QFileDialog.Options()
        input_file, _ = QFileDialog.getOpenFileName(self, "Choose File", "", "Markup files (*.xml *.json *yml)", options=options)

        if self.loaderThread is None or not self.loaderThread.is_alive():
            self.loaderThread = threading.Thread(target=self.emitter.sendInput(Path(input_file)))
            self.input_file_button.setText(f'{self.receiver.input.name} has been chosen.')

    def checkIfSuffixGiven(self, filename):
        """Verifies what kind of input user might want."""
        if '.xml' in filename:
            self.emitter.sendOutput_name(filename)
        elif '.json' in filename:
            self.emitter.sendOutput_name(filename)
        elif '.yml' in filename:
            self.emitter.sendOutput_name(filename)
        else:
            self.emitter.sendOutput_no_suffix(filename)

    def getOutputFileName(self):
        """Takes given name from the text field."""
        text = self.output_file_name.text()
        self.output_file_name.setPlaceholderText(text)
        self.output_file_name.setEnabled(False)
        self.checkIfSuffixGiven(text)

    def JSONConversion(self):
        if self.converterThread is None or not self.converterThread.is_alive():
            self.converterThread = threading.Thread(target=self.convertToJSON())

    def convertToJSON(self):

            if self.receiver.output_no_suffix != '':
                self.emitter.sendOutput_name(self.receiver.output_no_suffix + '.json')
            self.emitter.sendOutput(self.receiver.output_dir / self.receiver.output_name)

            try:
                inputControl = InputControl(self.receiver.input, self.receiver.output)
                GenerateOutput(self.receiver.input.suffix, self.receiver.output, inputControl.parsed_data)
            except InputControlFailed as e:
                self.convert_to_JSON.setStyleSheet('background-color: red; color: white;')
                self.convert_to_JSON.setText(str(e))

    def XMLConversion(self):
        if self.converterThread is None or not self.converterThread.is_alive():
            self.converterThread = threading.Thread(target=self.convertToXML())

    def convertToXML(self):

        if self.receiver.output_no_suffix != '':
            self.emitter.sendOutput_name(self.receiver.output_no_suffix + '.xml')
        self.emitter.sendOutput(self.receiver.output_dir / self.receiver.output_name)

        try:
            inputControl = InputControl(self.receiver.input, self.receiver.output)
            GenerateOutput(self.receiver.input.suffix, self.receiver.output, inputControl.parsed_data)
        except InputControlFailed as e:
            self.convert_to_XML.setStyleSheet('background-color: red; color: white;')
            self.convert_to_XML.setText(str(e))

    def YAMLConversion(self):
        if self.converterThread is None or not self.converterThread.is_alive():
            self.converterThread = threading.Thread(target=self.convertToYAML())

    def convertToYAML(self):

        if self.receiver.output_no_suffix != '':
            self.emitter.sendOutput_name(self.receiver.output_no_suffix + '.yml')
        self.emitter.sendOutput(self.receiver.output_dir / self.receiver.output_name)

        try:
            inputControl = InputControl(self.receiver.input, self.receiver.output)
            GenerateOutput(self.receiver.input.suffix, self.receiver.output, inputControl.parsed_data)
        except InputControlFailed as e:
            self.convert_to_YAML.setStyleSheet('background-color: red; color: white;')
            self.convert_to_YAML.setText(str(e))

    def outputDir(self):
        if self.outputThread is None or not self.outputThread.is_alive():
            self.outputThread = threading.Thread(target=self.chooseOutputDir())
            self.output_file_button.setText(f'{self.receiver.output_dir} has been chosen.')


    def chooseOutputDir(self):
        directory = QFileDialog.getExistingDirectory(self, "Open Directory",
                                       "/home",
                                       QFileDialog.ShowDirsOnly
                                       | QFileDialog.DontResolveSymlinks)

        self.output_file_button.setText(f'{directory} has been chosen.')
        self.emitter.sendOutput_dir(Path(directory))
        self.process()

    def process(self):
        if self.receiver.output_name != '' and self.receiver.output_no_suffix == '':
            self.suffixPresent()
        elif self.receiver.output_name == '' and self.receiver.output_no_suffix != '':
            self.suffixAbsent()

    def suffixPresent(self):
        self.emitter.sendOutput(self.receiver.output_dir / self.receiver.output_name)
        print(self.receiver.output)
        if self.receiver.output.suffix == '.xml':
            self.convert_to_XML.setEnabled(True)
        if self.receiver.output.suffix == '.json':
            self.convert_to_JSON.setEnabled(True)
        if self.receiver.output.suffix == '.yml':
            self.convert_to_YAML.setEnabled(True)

    def suffixAbsent(self):
        if self.receiver.input.suffix == '.xml':
            self.convert_to_XML.setEnabled(False)
            self.convert_to_JSON.setEnabled(True)
            self.convert_to_YAML.setEnabled(True)
        if self.receiver.input.suffix == '.json':
            self.convert_to_JSON.setEnabled(False)
            self.convert_to_XML.setEnabled(True)
            self.convert_to_YAML.setEnabled(True)
        if self.receiver.input.suffix == '.yml':
            self.convert_to_YAML.setEnabled(False)
            self.convert_to_XML.setEnabled(True)
            self.convert_to_JSON.setEnabled(True)

