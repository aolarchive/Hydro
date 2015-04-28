__author__ = 'yanivshalev'

import hashlib
import os
import inspect

def create_cache_key(fingerprint):
    return hashlib.md5(fingerprint).hexdigest()

def get_directory_from_search_path(given_search_path, file_name, lowest_class_instance):
    # get the relevant directory for a file from a list of inherited classes
    found_dir = False
    for stack_class_instance in given_search_path:
        dir_path = os.path.dirname(inspect.getabsfile(stack_class_instance))
        # The chosen directory has to have a conf.py file
        conf_file_path = '%s/%s'%(dir_path,file_name)
        if (os.path.exists(conf_file_path)) or (lowest_class_instance == stack_class_instance):
            found_dir = True
            break
        #TODO: make it work when no path is sent / when it didn't find the file
    return stack_class_instance.__module__, os.path.dirname(inspect.getabsfile(stack_class_instance)), found_dir
