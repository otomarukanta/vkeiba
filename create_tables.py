from sqlalchemy import create_engine
import json
from crawler import model

with open('conf/db.json', 'r') as f:
    string = 'postgresql+psycopg2://{user}:{passwd}@{host}/{db}'
    engine = create_engine(string.format(**json.load(f)), echo=True)

model.RaceResult.metadata.create_all(engine)
model.RaceInfo.metadata.create_all(engine)
