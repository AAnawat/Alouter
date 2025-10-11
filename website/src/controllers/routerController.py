from ..use_cases.addRouter import AddRouter
from ..use_cases.getAllRouter import GetAllRouter

class RouterController:
    def __init__(self, dbConnector):
        self.addRouterUseCase = AddRouter(dbConnector["credential"])
        self.getAllRoutersUseCase = GetAllRouter(dbConnector["credential"])

    def addRouter(self, name, host, username, password):
        try:
            result = self.addRouterUseCase(name, host, username, password)
            return result
        except Exception as e:
            raise e

    def getAllRouters(self):
        try:
            routers = self.getAllRoutersUseCase()
            return routers
        except Exception as e:
            raise e