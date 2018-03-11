import json

from db import PostgresDb
from expects import expect, equal, have_len, have_keys, have_key
from mamba import description, before, it

from app import app

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
        load_data()
        self.client = app.test_client()
    with after.all:
        clean_db()

    with context("When listing"):

        with it("returns only apartments in the bounding box"):
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
            response = self.client.get('/apartments?la=3&lo=3&s=2&r=2&a=60')
            expect(response.status_code).to(equal(200))
            apartments = json.loads(response.get_data().decode())
            expect(apartments).to(have_len(0))

        with it("returns only apartments with +-1 rooms"):
            response = self.client.get('/apartments?la=1&lo=0&s=2&r=1&a=60')
            expect(response.status_code).to(equal(200))
            apartments = json.loads(response.get_data().decode())
            expect(apartments).to(have_len(1))
            expect(apartments[0]['rooms']).to(equal(2))

        with it("returns only apartments with +-20% area"):
            response = self.client.get('/apartments?la=1&lo=0&s=2&r=2&a=70')
            expect(response.status_code).to(equal(200))
            apartments = json.loads(response.get_data().decode())
            expect(apartments).to(have_len(1))
            expect(apartments[0]['area']).to(equal('60'))

    with context("When handling content negotiation"):

        with it("returns json by default"):
            response = self.client.get('/apartments')
            expect(response.status_code).to(equal(200))
            expect(response.mimetype).to(equal('application/json'))

        with it("returns json if 'application/json'"):
            response = self.client.get('/apartments',
                                       headers={'Accept': 'application/json'})
            expect(response.status_code).to(equal(200))
            expect(response.mimetype).to(equal('application/json'))

        with it("returns csv if 'text/csv'"):
            response = self.client.get('/apartments',
                                       headers={'Accept': 'text/csv'})
            expect(response.status_code).to(equal(200))
            expect(response.mimetype).to(equal('text/csv'))
            data = response.get_data().decode()
            lines = data.split('\n')
            expect(lines[0]).to(equal("longitude,latitude,rooms,area"))
            expect(lines[1:]).to(have_len(4))

        with it("returns pdf if 'application/pdf'"):
            response = self.client.get('/apartments',
                                       headers={'Accept': 'application/pdf'})
            expect(response.status_code).to(equal(200))
            expect(response.mimetype).to(equal('application/pdf'))

        with it("returns unsupported media type if so"):
            response = self.client.get('/apartments',
                                       headers={'Accept': 'invalid/mimetype'})
            expect(response.status_code).to(equal(415))
            expect(response.get_data().decode()).to(equal('Unsupported Media Type'))
