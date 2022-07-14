# Distributed component that can be discovered and processes messages

from abc import abstractmethod

from aiko_services import *

__all__ = ["Service", "ServiceImpl", "ServiceImpl2"]

class Service(ServiceProtocol):
    Interface.implementations["Service"] = "aiko_services.service.ServiceImpl"

#   @abstractmethod
#   def service_0(self):
#       pass

class ServiceImpl(Service):
    def __init__(self, implementations):
        pass

#   def service_0(self):
#       print("ServiceImpl.service_0()")

class ServiceImpl2(Service):  # TODO: Move into "../examples/"
    def __init__(self, service_parameter_1):
        print(f"ServiceImpl2.__init__({service_parameter_1})")

    def service_0(self):
        print("ServiceImpl2.service_0()")
