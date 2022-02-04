# Copyright (c) 2022 aerocyber
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


import os
from base64 import b64encode, b64decode
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes


def encrypt(plain_text, password):
    """Encrypt the database.

    Args:
        plain_text (str): The database (as string) to be encrypted.
        password (str): The password with which the database will be encrypted.

    Returns:
        dict: Necessary information to decrypt the database.
    """
    # generate a random salt
    salt = get_random_bytes(AES.block_size)

    # use the Scrypt KDF to get a private key from the password
    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)

    # create cipher config
    cipher_config = AES.new(private_key, AES.MODE_GCM)

    # return a dictionary with the encrypted text
    cipher_text, tag = cipher_config.encrypt_and_digest(
        bytes(plain_text, 'utf-8'))
    return {
        'cipher_text': b64encode(cipher_text).decode('utf-8'),
        'salt': b64encode(salt).decode('utf-8'),
        'nonce': b64encode(cipher_config.nonce).decode('utf-8'),
        'tag': b64encode(tag).decode('utf-8')
    }


def decrypt(enc_dict, password):
    """Decrypt the database.

    Args:
        enc_dict (dict): The dictionary with the encrypted database and the 
                         necessary information to decrypt it.
        password (str): Password with which the database was encrypted.

    Returns:
        str: Decrypted database as string.
    """
    # decode the dictionary entries from base64
    salt = b64decode(enc_dict['salt'])
    cipher_text = b64decode(enc_dict['cipher_text'])
    nonce = b64decode(enc_dict['nonce'])
    tag = b64decode(enc_dict['tag'])

    # generate the private key from the password and salt
    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)

    # create the cipher config
    cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)

    # decrypt the cipher text
    decrypted = cipher.decrypt_and_verify(cipher_text, tag)

    return decrypted

# Code credits: https://hackernoon.com/how-to-use-aes-256-cipher-python-cryptography-examples-6tbh37cr
