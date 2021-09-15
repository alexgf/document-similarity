from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, ForeignKey, func

Base = declarative_base()

class Norm(Base):
    __tablename__ = 'norms'

    id = Column(Integer, primary_key=True)
    type = Column(Integer)
    url = Column(String)
    title = Column(String)
    content = Column(Text)
    processing_date = Column(DateTime)

    def __repr__(self):
        return f'Norm {self.url}'

    @classmethod
    def find_not_processed(cls, session, type):
        return session.query(cls).filter(cls.type==type, cls.processing_date == None).all()

    @classmethod
    def find_by_url(cls, session, url):
        return session.query(cls).filter_by(url=url).first()


class Control(Base):
    __tablename__ = 'controls'

    id = Column(Integer, primary_key=True)
    type = Column(Integer)
    start_time = Column(DateTime)
    finish_time = Column(DateTime)
    last_date_processed = Column(Date)

    @classmethod
    def find_last_date_processed(cls, session, type):
        return session.query(func.max(cls.last_date_processed)).filter(type==type).first()[0]


class DB:
    def __init__(self):
        self.engine = create_engine('sqlite:///norms.db', echo=False)
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        Base.metadata.create_all(self.engine)

    def add(self, item, commit=False):
        session = self.Session()
        session.add(item)
        session.commit()

    def session(self):
        return self.Session()

    def close(self):
        self.Session().close_all()
        self.engine.dispose()


class DocumentType:
    BNDES = 1
    CMN = 2