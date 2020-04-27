from libs.controller import Controller
from flask import request


class Route(Controller):
    route_id = None

    def get_routes(self):
        query = ["select * from routes limit 5"]
        result = self.conn.execute(query)
        if len(result) != 0:
            self.route_id = result[0]["route_id"]

        return result

    def get_stops_by_route(self):
        if request.method == 'GET':
            if request.args.get('route_id'):
                self.route_id = request.args.get('route_id')

            query = ["select distinct d.*\
                        from routes a\
                        inner join trips b on a.route_id = b.route_id\
                        inner join stop_times c on c.trip_id = b.trip_id\
                        inner join stops d on d.stop_id = c.stop_id\
                      where a.route_id = {0}".format(self.route_id)]
            return self.conn.execute(query)
        return []

    def get_stops_locations_by_route(self):
        data = self.get_stops_by_route()
        stops = []
        if len(data) != 0:
            for row in data:
                stops.append([row["stop_name"], row["stop_lat"], row["stop_lon"]])

        return stops

