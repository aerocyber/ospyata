# Copyright (c) 2021 aerocyber
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""
   Manage osmations: add, delete, edit, view.
"""

def addOsmation(db: list, name: str, url: str, cat=None):
    """Add osmation to the included osmations.

    Args:
        db (list): List of osmations.
        name (str): Name associated with the url.
        url (str): Url associated with the name.
        cat ((None OR list), optional): Categories to which the osmation belongs to. Defaults to None.

    Raises:
        TypeError: Invalid type.

    Returns:
        list: List of osmations.
    """
    dat = {
        "Name": name,
        "URL": url
    }
    if cat != None:
        if type(cat) is not list:
            raise TypeError("{cat} is expected to be of type list.".format(
                cat=cat
            ))
        dat["Categories"] = cat
    db.append(dat)
    return db

def delOsmation(db: list, name: str):
    """Delete an osmation with the name as given.

    Args:
        db (list): List of osmations.
        name (str): Name of osmation.

    Returns:
        db: List of osmations with name removed.
    """
    for i in db:
        if name == i["Name"]:
            _ = db.pop(db.index(i))
            break
    return db

def modName(name: str, db: list, newName: str):
    """Change the name of osmation.

    Args:
        name (str): Old name of osmation.
        db (list): List of osmations.
        newName (str): New name of osmation.

    """
    for i in db:
        if i["Name"] == name:
            i["Name"] = newName
            break


def changeURL(name: str, newUrl: str, db: str):
    """Change URL of osmation.

    Args:
        name (str): Name to which the new url is to be associated with.
        newUrl (str): [description]
        db (list): List of osmations.
    """
    for i in db:
        if i["Name"] == name:
            i["URL"] = newUrl
            break

def remByName(name: str, db: list):
    """Delete osmation by name

    Args:
        name (str): Name of osmation to delete.
        db (list): List of osmations.
    """
    for i in db:
        if i["Name"] == name:
            index = db.index(i)
            _ = i.pop(index)

