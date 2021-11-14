from base_application_resource import BaseRDBApplicationService
from database_service.rdb_service import RDBService


class LeadService(BaseRDBApplicationService):

    def __init__(self):
        super().__init__()
    
    @classmethod
    def get_database_info(cls):
        return 'talking_potatoes', 'leads'

    @classmethod
    def get_by_id(cls, id):
        template = {'id': id}
        res = LeadService.get_by_template(template)
        return res

    @classmethod
    def add_new_lead(cls, create_data):
        schema, table = LeadService.get_database_info()
        res = RDBService.create(schema, table, create_data)
        return res
    
    @classmethod
    def update_lead(cls, update_data):
        schema, table = LeadService.get_database_info()
        res = RDBService.update(schema, table, update_data)
        return res
    
    @classmethod
    def delete_by_id(cls, id):
        schema, table = LeadService.get_database_info()
        template = {'id': int(id)}
        res = RDBService.delete_by_template(schema, table, template)
        return res
