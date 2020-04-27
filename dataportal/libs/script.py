import hashlib
from time import gmtime, strftime

class Script(object):
    @staticmethod
    def encode(str):
        md5 = hashlib.md5()
        md5.update(bytes(str, 'utf-8'))
        return md5.hexdigest()

    @staticmethod
    def getfilename(prefix):
        return prefix+'_'+strftime("%Y%m%d%H%M%S", gmtime())
