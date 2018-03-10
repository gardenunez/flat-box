import json

from expects import expect, equal, have_len, have_keys, have_key

from app import app
from mamba import description, before, it

from db import PostgresDb


CONNECTION_STR = 'postgresql://postgres:postgres@db/flat_box'


def clean_db():
    db = PostgresDb(connection_str=CONNECTION_STR)
    db.execute_non_query("TRUNCATE TABLE apartments RESTART IDENTITY CASCADE")


def load_data():
    db = PostgresDb(connection_str=CONNECTION_STR)
    db.execute_non_query("INSERT INTO apartments(lat, lon, rooms, area) VALUES "
                         "(1, 1, 2, 50),"
                         "(1, -1, 3, 60),"
                         "(-1, 1, 3, 70),"
                         "(-1, -1, 2, 50)")

with description("App spec"):
    with before.each:
        clean_db()
        self.client = app.test_client()
    with after.all:
        clean_db()

    with it("returns only apartments in the bounding box"):
        load_data()
        response = self.client.get('/apartments?la=1&lo=0&s=2&r=2&a=60')
        expect(response.status_code).to(equal(200))
        apartments = json.loads(response.get_data().decode())
        expect(apartments).to(have_len(2))
        for flat in apartments:
            expect(flat).to(have_key("lat", '1'))
            if flat['lon'] == '1':
                expect(flat).to(have_keys({"rooms": 2, "area": '50'}))
            else:
                expect(flat).to(have_keys({"rooms": 3, "area": '60'}))

    with it("returns empty list when out of the bounding box"):
        load_data()
        response = self.client.get('/apartments?la=3&lo=3&s=2&r=2&a=60')
        expect(response.status_code).to(equal(200))
        apartments = json.loads(response.get_data().decode())
        expect(apartments).to(have_len(0))

    with it("returns only apartments with +-1 rooms"):
        load_data()
        response = self.client.get('/apartments?la=1&lo=0&s=2&r=1&a=60')
        expect(response.status_code).to(equal(200))
        apartments = json.loads(response.get_data().decode())
        expect(apartments).to(have_len(1))
        expect(apartments[0]['rooms']).to(equal(2))

    with it("returns only apartments with +-20% area"):
        load_data()
        response = self.client.get('/apartments?la=1&lo=0&s=2&r=2&a=70')
        expect(response.status_code).to(equal(200))
        apartments = json.loads(response.get_data().decode())
        expect(apartments).to(have_len(1))
        expect(apartments[0]['area']).to(equal('60'))
