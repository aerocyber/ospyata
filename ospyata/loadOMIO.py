# Copyright (c) 2021 aerocyber
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import json
import hashlib

"""Decode and decrypt .omio file which contain osmations."""

class InValidOMIO(Exception):
    """Exception raised if the .omio file is invalid.

    Args:
        Exception : file path and message.
    """
    
    def __init__(self, file, message="The omio file does not meet the osmata guidelines."):
        self.file =  file
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.file} -> {self.message}'

def validateAndOpen(OMIO_Path):
    """validate OMIO file and if valid, return data and header.

    Args:
        OMIO_Path (str): Path to .omio file.

    Raises:
        InValidOMIO: Exception if the omio file is not valid.
        
    Returns:
        header (dict): Information stored in the OMIO file.
        data (list): The osmations!
    """
    file = os.path.normpath(
            os.path.normcase(
                OMIO_Path
            )
        ) # Normalize path to omio file.
    f = open(
        file, 'r'
    )
    dat = json.load(f)
    f.close()
    if type(dat) is not dict: # Make sure the type of dat is dict
        raise InValidOMIO(file=file, message="The type of data MUST be dict.")
    data = dat["Data"]
    if type(data) is not list:
        raise InValidOMIO(file=file, message="Data in the key Data must be a list of dict.")
    for i in data:
        if type(i) is not dict:
            raise InValidOMIO(file=file, message="Each data INSIDE the Data list MUST be of type dict")
    try:
        header = dat["Header"]
    except KeyError():
        raise InValidOMIO(file=file, message="Header for the .omio file is missing...")
    else:
        sha256Data = hashlib.sha256(data)
        if sha256Data != header["SHA-256"]:
            raise InValidOMIO(file=file, message="Data Integrity check failed.")
        return header, data
