# facade_singleton.py
from .data_service import Facade, Subsystem1, Subsystem2, Subsystem3

class FacadeSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._initialize(cls._instance)
        return cls._instance

    @classmethod
    def _initialize(cls, instance):
        if not hasattr(instance, 'facade'):
            instance.subsystem1 = Subsystem1()
            instance.subsystem2 = Subsystem2()
            instance.subsystem3 = Subsystem3()
            instance.facade = Facade(
                instance.subsystem1,
                instance.subsystem2,
                instance.subsystem3
            )
            instance.facade.operation()

    @classmethod
    def get_facade(cls):
        if cls._instance is None:
            cls()
        return cls._instance.facade
