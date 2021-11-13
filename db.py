from sqlalchemy import create_engine


class Database:
    def __init__(self):
        self.engine = create_engine('postgresql+psycopg2://postgres:postgres@35.238.149.103/tp')

    def get_all_leads(self):
        result = self.engine.execute(
            '''select * from thumbtack.test;'''
        )

        return result
