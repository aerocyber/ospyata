# Copyright (c) 2021 aerocyber
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import json
import hashlib

"""Write OMIO files."""

def createOMIO(db, outfile, header=None):
    """Create OMIO in a standard way.

    Args:
        db (list): Database: List of dict.
        outfile (str): Path to file to which the osmations are written. If file exist, it is rewritten.
        header (dict, optional): Additional data to be included in header. Defaults to None.

    Raises:
        TypeError: For every invalid types at the required positions.

    """
    if type(db) is not list:
        raise TypeError("{db} is expected to be of type list.".format(db=db))
    for i in db:
        if type(i) is not dict:
            raise TypeError("{i} in {db} is expected to be of type dict".format(
                i = i,
                db = db
            ))
    headers = {}
    if header != None:
        if type(header) is not dict:
            raise TypeError("{header} is expected to be None or of type dict.".format(
                header=header
            ))
        if "SHA-256" in header.keys():
            raise ValueError("{header} is not expected to have user defined SHA-256.".format(
                header = header
            ))
        headers.update(header)
    headers["SHA-256"] = hashlib.sha256(db) # For ospyata and other osmation bindings to validate data integrity.
    data = {"Data": db}
    omioFormat = {}
    omioFormat.update(headers)
    omioFormat.update(data)
    file = os.path.normcase(
        os.path.normpath(
            outfile
        )
    )
    try:
        f = open(file, 'w')
        f.write(json.dumps(omioFormat))
        f.close()
    except Exception as e:
        raise e
