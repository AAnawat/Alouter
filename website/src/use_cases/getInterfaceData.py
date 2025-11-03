class GetInterfaceData:
    def __init__(self, dbConnector):
        self.connection = dbConnector

    def __call__(self, router_ip):
        data = self.connection.find_one(
            {"router_ip": router_ip},
            sort=[("timestamp", -1)]
        )
        return data