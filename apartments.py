import psycopg2

def get_apartments(db):
    return db.execute("SELECT * FROM apartments limit 10")

