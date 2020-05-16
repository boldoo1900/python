from libs.mysqldb import DB

class Controller(object):
    conn = None

    def __init__(self):
        # db connection object
        self.conn = DB()
