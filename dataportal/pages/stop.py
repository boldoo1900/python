from libs.controller import Controller
from flask import request


class Stop(Controller):
    stop_id = None

    def get_stations(self):
        query = ["select * from station"]
        return self.conn.execute(query)

    def get_stop_by_id(self):
        if request.method == 'GET':
            if request.args.get('stop_id'):
                self.stop_id = request.args.get('stop_id')

            query = ["select * from stops where stop_id = '{0}'".format(self.stop_id)]
            return self.conn.execute(query)
        return []

