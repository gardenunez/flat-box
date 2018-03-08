import psycopg2

def get_apartments(db):
    return db.execute("SELECT * FROM apartments limit 10")

def load_apartments(db):
    return db.execute("INSERT INTO apartments(lat, lon, rooms, area) \
                      SELECT random()::numeric, random()::numeric, (random()*10)::integer, \
                             (random()*100)::numeric FROM generate_series (1,10);")

