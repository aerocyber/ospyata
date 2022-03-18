# Copyright (c) 2021-present aerocyber
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""
   Manage osmations: add, delete, edit, view.
"""


import json
import validators


class Osmata:

    def __init__(self, database) -> None:
        self.db = database

    def add(self, name: str, url: str, category: list = []):
        """Add osmation to database.

        Args:
            name (str): Name associated with osmation.
            url (str): Url associated with osmation.
            category (list, optional): Categories. Defaults to [].
        """
        _name = self.check_existance(name)
        if _name["Type"] == "Exists":
            return {
                "Code": "Error",
                "On": name,
                "Type": "Exists"
            }
        _url_validation = self.check_url(url)  # validate url
        if _url_validation["Code"] == "Error":
            return _url_validation

        _url = self.check_existance(url)
        if _url["Type"] == "Exists":
            return {
                "Code": "Error",
                "On": url,
                "Type": "Exists"
            }

        self.db[name] = {
            "URL": url,
            "Category": category
        }
        return {
            "Code": "Success",
            "On": self.db,
            "Type": "Added"
        }

    def delete(self, name: str):
        """Delete osmation from database.

        Args:
            name (str): Name associated
        """
        if name in self.db:
            del self.db[name]
            return {
                "Code": "Success",
                "On": self.db,
                "Type": "Deleted"
            }
        return {
            "Code": "Error",
            "On": name,
            "Type": "Does not exist"
        }

    def edit(self, old_name: str, new_name: str, url: str, category: list = []):
        """Edit osmation in database.

        Args:
            old_name (str): Old name associated with osmation.
            new_name (str): New name associated with osmation.
            url (str): Url associated with osmation.
            category (list, optional): Categories. Defaults to [].
        """
        if old_name in self.db:
            _name = self.check_existance(new_name)
            if _name["Type"] == "Exists":
                return {
                    "Code": "Error",
                    "On": new_name,
                    "Type": "Exists"
                }
            _url_validation = self.check_url(url)
            if _url_validation["Code"] == "Error":
                return _url_validation
            _url = self.check_existance(url=url)
            if _url["Type"] == "Exists":
                return {
                    "Code": "Error",
                    "On": url,
                    "Type": "Exists"
                }
            # Delete old name
            del self.db[old_name]
            # Add new name
            self.db[new_name] = {
                "URL": url,
                "Category": category
            }
            return {
                "Code": "Success",
                "On": self.db,
                "Type": "Edited"
            }
        return {
            "Code": "Error",
            "On": old_name,
            "Type": "Does not exist"
        }

    def get(self, name: str):
        """Get osmation from database.

        Args:
            name (str): Name associated
        """
        if name in self.db:
            return {
                "Code": "Success",
                "On": self.db[name],
                "Type": "Found"
            }
        return {
            "Code": "Error",
            "On": name,
            "Type": "Does not exist"
        }

    def get_all(self):
        """Get all osmations from database."""
        return {
            "Code": "Success",
            "On": self.db,
            "Type": "Found"
        }

    def check_existance(self, name=False, url=False):
        """Check if osmation exists in database.

        Args:
            name (str): Name associated
            url (str): Url associated
        """
        if name in self.db:
            return {
                "Code": "Success",
                "On": name,
                "Type": "Exists"
            }
        __url = []
        for _name in self.db:
            __url.append(self.db[_name]["URL"])

        if url in __url:
            return {
                "Code": "Success",
                "On": url,
                "Type": "Exists"
            }
        if name != False:
            return {
                "Code": "Error",
                "On": name,
                "Type": "Does not exist"
            }
        if url != False:
            return {
                "Code": "Error",
                "On": url,
                "Type": "Does not exist"
            }
        return {
            "Code": "Error",
            "On": "check_existance",
            "Type": "No name or url"
        }

    def check_url(self, url):
        """Check if url is valid.

        Args:
            url (str): Url
        """
        try:
            if validators.url(url.strip()):
                return {
                    "Code": "Success",
                    "On": url,
                    "Type": "Valid"
                }
        except:
            return {
                "Code": "Error",
                "On": url,
                "Type": "Invalid"
            }

    def export_as_omio(self):
        """Return omio file."""
        head = {
            "Omio Version": "2.0"
        }
        data = {
            "Data": self.db
        }
        Footer = {
            "End of DB": "True"
        }

        omio = {
            "Header": head,
            "Data": data,
            "Footer": Footer
        }

        return {
            "Code": "Success",
            "On": omio,
            "Type": "Created omio file format"
        }

    def open_omio_file(self, file_content: str):
        """Use the file_content and return the databse.

        Args:
            file_content (str): Content of the files.
        """
        _db = json.loads(file_content)
        try:
            if _db["Header"]["Omio Version"] != "2.0":
                return {
                    "Code": "Error",
                    "On": _db["Header"]["Omio Version"],
                    "Type": "Wrong version"
                }
            return {
                "Code": "Success",
                "On": _db["Data"],
                "Type": "Osmations"
            }
        except:
            return {
                "Code": "Error",
                "On": _db["Header"],
                "Type": "Errors in database"
            }

    def import_from_omio(self, file_content: str):
        """Use the file_content and import the database.

        Args:
            file_content (str): Content of the files.
        """
        _db = self.open_omio_file(file_content)
        if _db["Code"] == "Error":
            return _db
        self.db = _db["On"]
        return {
            "Code": "Success",
            "On": self.db,
            "Type": "Imported"
        }
