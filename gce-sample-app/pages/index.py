from libs.controller import Controller

class Index(Controller):
    def getReports(self):
        query = ["""
                select a.*, revenue/(cv*cpi)*100 as roas 
                    from (
                        select campaign_id, count(campaign_id) as cv, avg(cost) as cpi, 
                               ifnull(sum(revenue), 0) as revenue 
                            from conversion_mb a 
                            left join purchase_mb b on a.session_id = b.session_id 
                        group by campaign_id
                    ) a where a.campaign_id <> 0
                """]

        return self.conn.execute(query)

    def getConvertions(self):
        query = ["select * from conversion_mb"]
        return self.conn.execute(query)

    def getPurchases(self):
        query = ["select * from purchase_mb"]
        return self.conn.execute(query)