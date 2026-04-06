from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy import UniqueConstraint

Base = declarative_base()

class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=True)
    title = Column(String, nullable=False)
    money = Column(Integer, nullable=False)
    result = Column(Integer, nullable=False)
    meigara = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint('year', 'month', 'title'),
    )