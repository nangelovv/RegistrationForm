from data.users_models import Users, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from common.secret import tests_database


class TestsPreparation:
    def __init__(self):
        self.session = self.create_database()

    def create_database(self):

        engine = create_engine(tests_database)
        Base.metadata.create_all(bind=engine, tables=[
            Users.__table__,
        ])
        return sessionmaker(bind=engine)()