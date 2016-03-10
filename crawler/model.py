import json
from sqlalchemy import Column, Integer, String, Date, Time, Float
from sqlalchemy import create_engine
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


def init_tables():
    with open('conf/db.json', 'r') as f:
        string = 'postgresql+psycopg2://{user}:{passwd}@{host}/{db}'
        engine = create_engine(string.format(**json.load(f)), echo=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init_tables()
