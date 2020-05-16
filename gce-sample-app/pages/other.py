from libs.controller import Controller
from config.constants import Constants
import csv

class Other(Controller):
    def executeDDL(self):
        fd = open(Constants.SQL_DDL, 'r')
        sqlfile = fd.read()
        fd.close()
        
        sqlCommands = sqlfile.split(';')
        message = "SUCCESS"
        for command in filter(None,sqlCommands):
            command.rstrip()
            result = self.conn.execute(command)
            if result is False:
                return "FAIL!!!"

        return message

    def importCSV(self):
        message = "SUCCESS"
        with open(Constants.CSV_CONVERSION) as csvfile:
            data_conversion = csv.reader(csvfile, delimiter=",")
            next(data_conversion)

            values = []
            statement = "insert into conversion_mb(campaign_id, cvdt, session_id, cost, idfa) values"
            for row in data_conversion:            
                values.append("('{}', '{}', '{}', '{}', '{}')".format(row[0], row[1], row[2], row[3], row[4]))

            result = self.conn.execute("truncate table conversion_mb")
            if result is False:
                message = "FAIL!!!"

            query = statement + ",".join(values) + ";"
            result = self.conn.execute(query)
            if result is False:
                message = "FAIL!!!"

            # print(query)
        
        with open(Constants.CSV_PURCHASE) as csvfile:
            data_purchase = csv.reader(csvfile, delimiter=",")
            next(data_purchase)

            values = []
            statement = "insert into purchase_mb(evdt, session_id, revenue, idfa) values"
            for row in data_purchase:
                values.append("('{}', '{}', '{}', '{}')".format(row[0], row[1], row[2], row[3]))

            result = self.conn.execute("truncate table purchase_mb")
            if result is False:
                message = "FAIL!!!"

            query = statement + ",".join(values) + ";"
            result = self.conn.execute(query)
            if result is False:
                message = "FAIL!!!"

            # print(query)

        return message