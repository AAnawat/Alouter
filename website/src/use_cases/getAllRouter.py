class GetAllRouter:
    def __init__(self, dbConnector):
        self.connector = dbConnector

    def __call__(self, *args, **kwds):
        getResult = self.connector.find()
        output = map(
            lambda router: {
                "id": str(router["_id"]),
                "name": router["name"],
                "host": router["host"],
            },
            getResult,
        )
        if not output:
            raise Exception("Don't have Routers")
        return output
