from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from settings import debug_settings
from models import Student
from random import randint


# SQLAlchemy 中postgres 数据库地址格式
POSTGRES_PATTERN = 'postgresql://{login}:{password}@{host}:{port}/{dbname}'


def get_db_url(settings):
    """
    拼接数据库地址
    """
    return POSTGRES_PATTERN.format(
        login=settings['PSQL_ACCOUNT'],
        password=settings['PSQL_PASSWORD'],
        host=settings['PSQL_HOST'],
        port=settings['PSQL_PORT'],
        dbname=settings['PSQL_DBNAME']
    )


def get_db_engine(settings):
    """
    创建db engine
    """
    db_url = get_db_url(settings)
    engine = create_engine(db_url, echo=False)
    return engine


def get_db_session(settings):
    """
    db 的初始化
    """

    engine = get_db_engine(settings)
    # drop掉所有的表
    if settings['DROP']:
        print('初始化数据库...')
        Base.metadata.drop_all(bind=engine)
    # 根据model模型创建表
    Base.metadata.create_all(bind=engine)
    # 创建会话并返回  该会话用于数据库操作
    session = sessionmaker(bind=engine)
    return session()


def init_database():
      # 初始化数据库内容数据
        session = get_db_session(debug_settings)
        for i in range(20):
            new_user = Student('Bob' + str(i + 1), i + 1, 1.75, randint(1, 7))
            session.add(new_user)
            session.commit()

        # 关闭session:
        session.close()
