from sqlalchemy import create_engine, Column, Integer, String, VARCHAR, DateTime, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://board:board1pwd@localhost:5431/board')

Session = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)


class Ad(Base):
    __tablename__ = 'board_ads'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(255), nullable=False)
    description = Column(String)
    creation_time = Column(DateTime, server_default=func.now())
    user = Column(Integer, nullable=False)


Base.metadata.create_all()
