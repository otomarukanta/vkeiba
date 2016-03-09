from sqlalchemy import Column, Integer, String, Time, Float
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class RaceResult(Base):
    __tablename__ = 'race_result'

    race_id = Column(String, primary_key=True)
    row_id = Column(Integer, primary_key=True)
    final_position = Column(String)
    frame_number = Column(Integer)
    horse_number = Column(Integer)
    horse_id = Column(String)
    sex = Column(String)
    age = Column(String)
    jockey_id = Column(String)
    time = Column(Time)
    margin = Column(String)
    passing_position = Column(String)
    last_3f = Column(Time)
    jockey_weight = Column(Float)
    horse_weight = Column(Float)
    popularity = Column(Integer)
    odds = Column(Float)
    blinker = Column(String)

    def __str__(self):
        return '{},{}'.format(self.race_id, self.row_id)
