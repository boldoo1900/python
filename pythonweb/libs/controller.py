from libs.db import DB
from config.constants import Constants

class Controller(object):
    dbconn = None

    def __init__(self):
        self.dbconn = DB()