# Copyright (c) 2021 aerocyber
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import json
from . import encryptionManagement as eM

"""Decode and decrypt .omio file which contain osmations."""

class PasswordNotProvided(Exception):
    
    def __init__(self, pswd, message="Password required to open the selected osmation."):
        self.pswd =  pswd
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.pswd} -> {self.message}'

class inValidPassword(Exception):
    
    def __init__(self, pswd, message="Password verification failed."):
        self.pswd =  pswd
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.pswd} -> {self.message}'

def checkEncryption(file_path):
    f = open(
        os.path.normcase(
            os.path.normpath(file_path)
        )
    )
    dat = json.load(f)
    f.close()
    encryption = dat["Header"]["Encryption"]
    return encryption, dat

def decode(file_path, pswd=None):
    encryption, dat = checkEncryption(file_path)
    if encryption == "True":
        if pswd == None:
            raise PasswordNotProvided(pswd=pswd, message="Password required to open the selected osmation.")
        else:
            if "Verify Data" in dat["Encryption"].keys():
                verificationPass = eM.verifyData(tobeverified=(dat["Data"]), pswd=pswd)
                if verificationPass == True:
                    return eM.decrypt(data=(dat["Data"]), pswd=pswd)
                else:
                    raise inValidPassword(pswd, message="Password verification failed.")
            else:
                return eM.decrypt(data=(dat["Data"]), pswd=pswd)