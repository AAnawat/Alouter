class GetLogsData:
    def __init__(self, dbConnector):
        self.connection = dbConnector

    def __call__(self, router_ip):
        data = self.connection.find(
            {"router_ip": router_ip},
        )

        data = list(data)

        return data
