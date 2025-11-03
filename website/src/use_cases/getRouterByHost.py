class GetRouterByHost:
    def __init__(self, dbConnector):
        self.connection = dbConnector

    def __call__(self, router_ip):
        router = self.connection.find_one({"host": router_ip})
        if not router:
            raise Exception(f"Router with IP {router_ip} not found")
        return router
