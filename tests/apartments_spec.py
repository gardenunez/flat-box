from doublex import Stub, ANY_ARG
from expects import expect, equal, be_a, have_keys, have_len
from mamba import description, it, context, before

from apartments import get_apartments


def check_apartments(subject):
    expect(subject).to(be_a(list))
    expect(subject).to(have_len(2))
    for rec in subject:
        expect(rec).to(have_keys('area', 'lat', 'lon', 'rooms'))


with description("Apartments Spec"):
    with context("When no data"):
        with it("returns empty list"):
            with Stub() as db:
                db.execute_query(ANY_ARG).returns([])
            expect(get_apartments(db=db, longitude=1,
                                  latitude=1, side=1,
                                  rooms=1, area=1)).to(equal([]))
            expect(get_apartments(db=db)).to(equal([]))

    with context("When there is data"):
        with before.each:
            self.apartments = [
                {
                    "area": "irrelevant_area", "lat": "irrelevant_lat",
                    "lon": "irrelevant_lon", "rooms": "irrelevant_room"
                },
                {
                    "area": "irrelevant_area", "lat": "irrelevant_lat",
                    "lon": "irrelevant_lon", "rooms": "irrelevant_room"
                }
            ]
        with it("returns first apartments by default"):
            with Stub() as db:
                db.execute_query(ANY_ARG).returns(self.apartments)
            check_apartments(get_apartments(db=db))

        with it("returns first apartments if missing filters"):
            with Stub() as db:
                db.execute_query(ANY_ARG).returns(self.apartments)
            check_apartments(get_apartments(db=db, latitude=1, side=1, rooms=1, area=1))
            check_apartments(get_apartments(db=db, longitude=1, side=1, rooms=1, area=1))
            check_apartments(get_apartments(db=db, longitude=1, latitude=1, rooms=1, area=1))
            check_apartments(get_apartments(db=db, longitude=1, latitude=1, side=1, area=1))
            check_apartments(get_apartments(db=db, longitude=1, latitude=1, side=1, rooms=1))

        with it("returns list of apartments in bounding box"):
            with Stub() as db:
                db.execute_query(ANY_ARG).returns(self.apartments)
            check_apartments(get_apartments(db=db, longitude=0.1, latitude=0.2, side=1, rooms=1, area=1))
