import logging

from domain.unit_of_work import UnitOfWork

class SqlAlchemyUnitOfWork(UnitOfWork):

    def __init__(self, session):
        self.session = session
        self.committed = False

    def __enter__(self):
        pass

    def __exit__(self, exception_type, exception_value, traceback):
        if exception_type is not None:
            self.rollback()
            logging.info(f"Unexpected exception: {exception_type},\n"
                         f"Value exception:{exception_value},\n"
                         f" with traceback:{traceback}")
        else:
            self.commit()

    def commit(self):
        self.session.commit()
        self.committed = True

    def rollback(self):
        self.session.rollback()
