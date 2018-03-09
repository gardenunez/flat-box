from mamba import description, before, it

from db import PostgresDb


CONNECTION_STR = 'postgresql://postgres:postgres@db/flat_box'


def clean_db(db=None):
    if not db:
        db = PostgresDb(connection_str=CONNECTION_STR)
    db.execute_non_query("TRUNCATE TABLE \"apartments\" RESTART IDENTITY CASCADE")


with description("App spec"):
    with before.each:
        clean_db()
    with it("returns apartments in the bounding box only"):
        pass
