# -*- encoding: utf-8 -*-

from generatefiles.config import CONFIG
from itertools import count
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine, Connection
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.engine.strategies import PlainEngineStrategy
import transaction
from zope.sqlalchemy import ZopeTransactionExtension, mark_changed

class ROUTINEConnection(Connection):
    MAX_RETRY = CONFIG.get_attribute('connection', 'max_retry', 4, int)

    def __init__(self, engine, connection=None, close_with_result=False,
                 _branch=False, _execution_options=None):
        super(ROUTINEConnection, self).__init__(
            engine,
            connection,
            close_with_result,
            _branch,
            _execution_options
        )
        self._retry_count = count()

    def execute(self, object, *multiparams, **params):

        try:
            result = super(ROUTINEConnection, self).execute(
                object,
                *multiparams,
                **params
            )
            return result
        except Exception as e:
            raise e
        raise


class ConnectionEngine(Engine):
    _connection_cls = ROUTINEConnection


class ConnectionEngineStrategy(PlainEngineStrategy):
     name = 'rotina'
     engine_cls = ConnectionEngine

ConnectionEngineStrategy()

class DBTransaction(object):
    def __init__(self, db):
        self.db = db

    def __enter__(self):
        mark_changed(self.db)
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            transaction.abort()
        else:
            transaction.commit()

def make_session():
    connection = CONFIG.get_section('connection')
    session = scoped_session(
        sessionmaker(
            bind=create_engine(
                'mssql+pyodbc://{user}:{password}@{dsn}'.format(
                    user=connection['username'],
                    password=connection['password'],
                    dsn=connection['dsn'],
                ),
                encoding='latin1',
                convert_unicode=True,
                supports_unicode_binds=False,
                strategy='rotina',
            ),
            extension=ZopeTransactionExtension(),
        ),
    )
    return session

SCHEMA = CONFIG.get_attribute('connection', 'schema') or 'dbo'
session_factory = make_session()