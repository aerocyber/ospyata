# Copyright (c) 2021 aerocyber
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""
   Manage osmations: add, delete, edit, view.
"""

import hashlib
import json
import validators
from . import encryption


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
            _url = self.check_existance(url)
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

    def encryptDB(self, pswd: str):
        """Encrypt database with AES Encryption."""
        _result = encryption.encrypt(json.dumps(self.db), pswd)
        self.salt = _result["salt"]
        self.nonce = _result["nonce"]
        self.tag = _result["tag"]
        self.db = _result["cipher_text"]
        return _result

    def decryptDB(self, ciphertext, salt, tag, nonce, pswd: str):
        """Decrypt database with AES Encryption."""
        db = {
            'cipher_text': ciphertext,
            'salt': salt,
            'nonce': nonce,
            'tag': tag
        }
        _result = encryption.decrypt(db, pswd)
        self.db = json.loads(_result["db"])
        return _result

    def export_as_omio(self, encryption: bool, pswd=False):
        """Return omio file."""
        Extra_data = {
            "salt": self.salt,
            "nonce": self.nonce,
            "tag": self.tag
        }
        if encryption:
            if pswd == False:
                return {
                    "Code": "Error",
                    "On": encryption + " & " + pswd,
                    "Type": "No password"
                }
            if pswd == True:
                return {
                    "Code": "Error",
                    "On": pswd,
                    "Type": "Expected str got bool"
                }
            _result = self.encryptDB(json.dumps(self.db), pswd)
            self.db = _result["cipher_text"]
            encryption = "True"
            pshash = hashlib.sha256(pswd.encode('utf-8')).hexdigest()
        else:
            encryption = "False"
            pshash = ""
        head = {
            "Omio Version": "2.0",
            "Restricted": encryption,
            "Password Hash": pshash,
            "Extra Data": Extra_data
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

    def open_omio_file(self, file_content: str, pswd=False):
        """Use the file_content and return the databse, unencrypted.

        Args:
            file_content (str): Content of the files.
            pswd (str): Password.
        """
        _db = json.loads(file_content)
        try:
            if _db["Header"]["Omio Version"] != "2.0":
                return {
                    "Code": "Error",
                    "On": _db["Header"]["Omio Version"],
                    "Type": "Wrong version"
                }
            if _db["Header"]["Restricted"]:
                if not pswd:
                    return {
                        "Code": "Error",
                        "On": _db["Header"]["Restricted"],
                        "Type": "Password required"
                    }
                if pswd:
                    _result = self.decryptDB(
                        _db["Data"],
                        _db["Header"]["Extra Data"]["salt"],
                        _db["Header"]["Extra Data"]["tag"],
                        _db["Header"]["Extra Data"]["nonce"],
                        pswd
                    )
                    _data = json.loads(_result["db"])
                    return {
                        "Code": "Success",
                        "On": _data,
                        "Type": "Decrypted"
                    }
            if not _db["Header"]["Restricted"]:
                return {
                    "Code": "Success",
                    "On": _db["Data"],
                    "Type": "Unencrypted"
                }
        except:
            return {
                "Code": "Error",
                "On": _db["Header"],
                "Type": "Errors in database"
            }

    def import_from_omio(self, file_content: str, pswd=False):
        """Use the file_content and import the database.

        Args:
            file_content (str): Content of the files.
            pswd (str): Password.
        """
        _db = self.open_omio_file(file_content, pswd)
        if _db["Code"] == "Error":
            return _db
        self.db = _db["On"]
        return {
            "Code": "Success",
            "On": self.db,
            "Type": "Imported"
        }
