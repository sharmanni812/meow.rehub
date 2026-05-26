import os
from dotenv import load_dotenv
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()

__factory = None

def global_init(db_file):
    global __factory

    if __factory:
        return

    # 1. Загружаем переменные окружения из .env
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")

    # 2. Проверяем, задана ли серверная база данных
    if database_url:
        # Если есть ссылка на Postgres, используем её
        conn_str = database_url
    else:
        # Если ссылки нет, используем старую логику с локальным SQLite
        if not db_file or not db_file.strip():
            raise Exception("Укажите файл базы данных или настройте DATABASE_URL в .env")
        conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'

    # 3. Создаем движок (SQLAlchemy сама поймет, Postgres это или SQLite)
    engine = sa.create_engine(conn_str, echo=False)

    __factory = orm.sessionmaker(bind=engine)

    from . import tables
    SqlAlchemyBase.metadata.create_all(engine)

def create_session() -> Session:
    global __factory
    return __factory()