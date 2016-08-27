from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Student(Base):
    """
    学生数据模型
    """
    __tablename__ = 'stu'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(30), nullable=False)
    age = Column(Integer, nullable=False)
    height = Column(Float, nullable=False)
    grade = Column(Integer, nullable=False)

    def json_str(self):
        return {'id':self.id,'username':self.username,'age':self.age,
                'height':self.height,'grade':self.grade}

    def __init__(self, username, age, height, grade):
        self.username = username
        self.age = age
        self.height = height
        self.grade = grade

    def __repr__(self):
        return "<Student('%s')>" % (self.username)


class Admin(Base):
    __tablename__ = 'admin'

    id = Column(Integer, primary_key=True, autoincrement=True)
    admin_name = Column(String(30), nullable=False, unique=True)
    password = Column(String(30), nullable=False)

    def __init__(self, admin_name, password):
        self.admin_name = admin_name
        self.password = password

    def __repr__(self):
        return "<Admin('%s')>" % (self.admin_name)
