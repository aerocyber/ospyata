# Copyright (c) 2021 aerocyber
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""
   Manage osmations: add, delete, edit, view.
"""

def addOsmation(db, name, url, cat=None):
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
    # TODO: Add validation
    db.append(dat)
    return db