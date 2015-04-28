__author__ = 'yanivshalev'

import hashlib
import os
import inspect


def create_cache_key(fingerprint):
    return hashlib.md5(fingerprint).hexdigest()


def get_directory_from_search_path(given_search_path, file_name, topmost_class):
    # get the relevant directory for a file from a list of inherited classes
    for class_type in given_search_path:
        dir_path = os.path.dirname(inspect.getabsfile(class_type))
        # The chosen directory has to have a conf.py file
        conf_file_path = '%s/%s' % (dir_path, file_name)
        if (os.path.exists(conf_file_path)) or (topmost_class == class_type):
            return class_type.__module__, os.path.dirname(inspect.getabsfile(class_type)), True
        #TODO: make it work when no path is sent / when it didn't find the file
    return None, None, False
