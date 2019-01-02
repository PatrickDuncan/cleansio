""" Loads list of explicits from an encrypted file """

import os
from Crypto.Cipher import AES
import yaml

class Explicits():
    """ Object representing set of explicits"""
    def __init__(self):
        """ Decrypt encrypted list of explicits and return a set """
        encypted_file = open(self.get_explicits_path(), 'rb')
        decrypted_content = self.get_decrypted_content(encypted_file)
        encypted_file.close()

        yaml_content = yaml.load(decrypted_content)
        censored_words_list = yaml_content['explicits']
        self.set = set(censored_words_list)

    @classmethod
    def get_explicits_path(cls):
        """ Return path of encrypted explicits file """
        current_path = os.path.dirname(__file__)
        path_to_enc_file = os.path.join(current_path, '../data/explicits-list')
        return path_to_enc_file

    @classmethod
    def get_decrypted_content(cls, encrypted_file):
        """ Decrypt the encrypted file and return content as string """
        decryptor = AES.new('cleansio_sym_key', AES.MODE_CBC, 'cleansioCensorIV')
        content = ''

        while True:
            block = encrypted_file.read(16)
            if not block:
                break
            content += decryptor.decrypt(block).decode('utf-8')

        return content
