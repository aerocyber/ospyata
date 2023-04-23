# Copyright (c) 2021-present aerocyber
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import json
import validators
from typing import List
import pathlib


class OspyataException(Exception):
    pass


class Osmata:

    def __init__(self):
        self.db = {}  # Initialize the datastructure.

    def push(self, name: str, url: str, categories: List[str] = []):
        """Push a record to the datastructure.

        Args:
            name (str): The name (key) of the record.
            url (str): The URL (value) associated with the name (key).
            categories (str, optional): Categories to which the keypair is assigned to. Defaults to [].
        """

        # Validate url before anything else!
        try:
            self.validate_url(url)
        except Exception as e:
            # It is the application that deals with errors not the library. See Error_policy.md in the docs.
            raise e
        else:
            # Check existance. If exists, raise error for the application to solve. Else, add to self.db
            if self.check_existance(name=name):
                _msg = name + " exists in db."
                raise OspyataException(_msg)
            elif self.check_existance(url=url):
                _msg = url + " exists in db."
                raise OspyataException(_msg)
            else:
                self.db[name] = {
                    "URL": url,
                    "Categories": categories
                }

    def pop(self, name: str):
        """Delete a record from db matching name.

        Args:
            name (str): The name (key) associated with the record to be deleted.
        """

        # First, check its existance.
        if self.check_existance(name=name):
            del self.db[name]  # Yup, as simple as that.
        else:
            _msg = name + " do not exist in db."
            raise OspyataException(_msg)  # Either success or failure.

    def validate_omio(self, dat: str):
        """Validate an omio file

        Args:
            dat (str): The omio string.
        """
        # schema = {
        #     "$schema": "https://json-schema.org/draft/2020-12/schema",
        #     "$id": "https://example.com/product.schema.json",
        #     "title": "Osmations",
        #     "description": "A record of all bookmarks.",
        #     "type": "object",
        #     "properties": {
        #         "Name": {
        #             "description": "The unique identifier for a record.",
        #             "type": "string"
        #         },
        #         "URL": {
        #             "description": "URL associated with the Name.",
        #             "type": "string"
        #         },
        #         "Categories": {
        #             "description": "Tags for the Record",
        #             "type": "array",
        #             "items": {
        #                 "type": "string"
        #             }
        #         }
        #     },
        #     "required": ["Name", "URL"]
        # }
        # try:
        #     validate(instance=dat, schema=schema)
        # except Exception as e:
        #     return False
        # else:
        #     return True
        data = json.loads(dat)
        _keys = data.keys()
        _urls = []
        _is_cat_list = True
        for record in data:
            if isinstance(record, str):
                if isinstance(data[record], dict):
                    if "URL" in data[record].keys():
                        if "Categories" in data[record].keys():
                            if not isinstance(data[record]["Categories"], list):
                                return False
                            else:
                                try:
                                    _is_url = self.validate_url(data[record]["URL"])
                                except Exception:
                                    return False
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        return True



    def dumpOmio(self):
        return json.dumps(self.db)

    def loadOmio(self, omio_path):
        if pathlib.Path(omio_path).exists():
            f = open(omio_path, 'r')
            data = f.read()
            f.close()
            if self.validate_omio(dat=data):
                _json = json.loads(data)
                return _json
            else:
                raise OspyataException("Invalid omio file.")
        else:
            raise FileNotFoundError("The file: " + omio_path + " was not found.")

    def check_existance(self, name=False, url=False):
        """Check if osmation exists in database.

        Args:
            name (str | False): Name associated. Defaults to False.
            url (str | False): Url associated. Defaults to False.
        """
        if name == False:
            if url == False:
                raise OspyataException(
                    "Neither name nor url is present for existance checking.")
            else:
                _names = self.db.keys()
                for _name in _names:
                    if url == self.db[_name]["URL"]:
                        return True
                    else:
                        return False
        else:
            if url == True:
                raise OspyataException("Both name and url is present.")
            else:
                _names = self.db.keys()
                if name in _names:
                    return True
                else:
                    return False

    def validate_url(self, url):
        """Check if url is valid.

        Args:
            url (str): Url
        """
        try:
            if validators.url(url.strip()):
                return True
        except Exception as e:
            raise e
