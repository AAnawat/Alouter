from ..use_cases.addRouter import AddRouter
from ..use_cases.getAllRouter import GetAllRouter
from ..use_cases.getRouterByHost import GetRouterByHost
from ..use_cases.getInterfaceData import GetInterfaceData
from ..use_cases.getPerformanceData import GetPerformanceData
from ..use_cases.getLogsData import GetLogsData

class RouterController:
    def __init__(self, dbConnector):
        self.addRouterUseCase = AddRouter(dbConnector["credential"])
        self.getAllRoutersUseCase = GetAllRouter(dbConnector["credential"])
        self.getRouterByHostUseCase = GetRouterByHost(dbConnector["credential"])
        self.getInterfaceUseCase = GetInterfaceData(dbConnector["interface"])
        self.getPerformanceUseCase = GetPerformanceData(dbConnector["performance"])
        self.getLogsUseCase = GetLogsData(dbConnector["log"])


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

    def getRouterByHost(self, ip):
        try:
            router = self.getRouterByHostUseCase(ip)
            return router
        
        except Exception as e:
            raise e
    
    def getInterface_status(self, ip):
        try:
            interface_data = self.getInterfaceUseCase(ip)
            return interface_data

        except Exception as e:
            raise e

    def getPerformance(self, ip):
        try:
            performance_data = self.getPerformanceUseCase(ip)
            return performance_data
        
        except Exception as e:
            raise e

    def getLogging(self, ip):
        try:
            log_data = self.getLogsUseCase(ip)
            return log_data
        
        except Exception as e:
            raise e