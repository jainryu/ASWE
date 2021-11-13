from abc import ABC, abstractmethod
from database_service.rdb_service import RDBService


# interface
class BaseApplicationService(ABC):

    def __init__(self):
        pass

    @classmethod
    @abstractmethod
    def get_data_resource_info(self):
        pass

    @classmethod
    @abstractmethod
    def get_by_template(cls, template):
        pass


# mysql syntax
class BaseRDBApplicationService(BaseApplicationService):

    def __init__(self):
        pass

    @classmethod
    @abstractmethod
    def get_data_resource_info(self):
        pass

    @classmethod
    def get_by_template(cls, template):
        db_name, table_name = cls.get_data_resource_info()
        res = RDBService.find_by_template(db_name, table_name, template)
        return res
    
    @classmethod
    def delete_by_template(cls, template):
        schema, table = cls.get_data_resource_info()
        res = RDBService.delete_by_template(schema, table, template)
        return res
