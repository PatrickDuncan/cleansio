""" Loads list of explicits from an encrypted file """

from Crypto.Cipher import AES
import yaml
from utils import relative_path
from .file_loader import FileLoader

class Explicits():
    """ Object representing set of explicits"""
    def __init__(self, args):
        """ Decrypt encrypted list of explicits and return a set """
        self.set = self.__set(args)

    def __set(self, args):
        explicit_set = {}
        if args.user_list and args.combine_lists:
            internal_set = self.__internal_set()
            user_set = self.__user_set(args.user_list[0])
            explicit_set = internal_set.union(user_set)
        elif args.user_list:
            explicit_set = self.__user_set(args.user_list[0])
        else:
            explicit_set = self.__internal_set()
        return set(map(lambda e: e.lower(), explicit_set))

    def __internal_set(self):
        with open(self.__get_explicits_path(), 'rb') as file:
            decrypted_content = self.__get_decrypted_content(file)

        yaml_content = yaml.load(decrypted_content)
        return set(yaml_content['explicits'])

    @classmethod
    def __user_set(cls, user_list):
        return FileLoader(user_list).set

    @classmethod
    def __get_explicits_path(cls):
        """ Return path of encrypted explicits file """
        path_to_enc_file = relative_path('../data/explicits-list')
        return path_to_enc_file

    @classmethod
    def __get_decrypted_content(cls, encrypted_file):
        """ Decrypt the encrypted file and return content as string """
        decryptor = AES.new('cleansio_sym_key', AES.MODE_CBC, 'cleansioCensorIV')
        content = ''
        while True:
            block = encrypted_file.read(16)
            if not block:
                break
            content += decryptor.decrypt(block).decode('utf-8')
        return content
