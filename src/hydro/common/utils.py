__author__ = 'yanivshalev'

import hashlib

def create_cache_key(fingerprint):
    return hashlib.md5(fingerprint).hexdigest()