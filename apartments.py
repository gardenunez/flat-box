import psycopg2
from db import PostgresDb


CONNECTION_STR = 'postgresql://postgres:postgres@db/postgres'
DB = PostgresDb(connection_str=CONNECTION_STR)

def get_apartments(db=DB):
    return db.execute("SELECT * FROM apartments limit 10")

def load_apartments(db=DB):
    return db.execute("INSERT INTO apartments(lat, lon, rooms, area) \
                      SELECT random()::numeric, random()::numeric, (random()*10)::integer, \
                             (random()*100)::numeric FROM generate_series (1,10);")

