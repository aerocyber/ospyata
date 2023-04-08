# Copyright (c) 2021-present aerocyber
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import json
import validators


class OspyataException(Exception):
    pass


class Osmata:

    def __init__(self):
        db = {}  # Initialize the datastructure.

    def push(self, name: str, url: str, categories: str = []):
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
