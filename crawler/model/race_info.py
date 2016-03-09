from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class RaceInfo(Base):
    __tablename__ = 'race_info'

    race_id = Column(String, primary_key=True)
    race_date = Column(Date)
    times = Column(Integer)
    place = Column(String)
    days = Column(String)
    start_time = Column(String)
    race_name = Column(String)
    weather = Column(String)
    track_condition = Column(String)
    track_type = Column(String)
    rotation = Column(String)
    distance = Column(Integer)
    race_condition = Column(String)
    grade = Column(String)
    race_type = Column(String)
    money = Column(String)
