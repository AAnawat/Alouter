class AddRouter:
    def __init__(self, dbConnector):
        self.connection = dbConnector

    def __call__(self, name, host, username, password):
        insertResult = self.connection.insert_one({
            "name": name,
            "host": host,
            "username": username,
            "password": password
        })

        return insertResult
