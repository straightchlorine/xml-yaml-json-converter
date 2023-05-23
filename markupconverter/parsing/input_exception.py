#!/bin/python

class InputControlFailed(Exception):
    """Exception raised if validation in InputControl fails"""
    def __init__(self, message):
        super().__init__(message)
