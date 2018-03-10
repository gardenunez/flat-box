from decimal import Decimal

from db import PostgresDb

# TODO: move to environmnet variable
CONNECTION_STR = 'postgresql://postgres:postgres@db/flat_box'
DB = PostgresDb(connection_str=CONNECTION_STR)


def get_apartments(db=DB, longitude=None, latitude=None, side=None, rooms=None, area=None):
    if None in (longitude, latitude, side, rooms, area):
        return get_default_apartments(db)
    else:
        # TODO: refactor this.
        longitude = Decimal(longitude)
        latitude = Decimal(latitude)
        side = int(side)
        rooms = int(rooms)
        area = Decimal(area)
        return get_bounding_box_apartments(db, longitude, latitude, side, rooms, area)


def get_default_apartments(db):
    results = db.execute_query("SELECT lat, lon, rooms, area FROM apartments limit 10",
                               dict_cursor=True)
    return [dict(record) for record in results]


def load_apartments(db=DB):
    return db.execute_non_query("INSERT INTO apartments(lat, lon, rooms, area) \
                      SELECT random()::numeric, random()::numeric, (random()*10)::integer, \
                             (random()*100)::numeric FROM generate_series (1,10);")


def get_bounding_box_apartments(db, longitude, latitude, side, rooms, area):
    query = "SELECT lat, lon, rooms, area \
            FROM apartments a \
            WHERE " \
            "(%(latitude)s - %(half_side)s) <= a.lat AND a.lat <= (%(latitude)s + %(half_side)s) " \
            "AND ( (%(longitude)s - %(half_side)s) <= a.lon AND a.lon <= (%(longitude)s + %(half_side)s)) " \
            "AND (%(rooms)s - 1 <= a.rooms AND a.rooms <= %(rooms)s + 1) " \
            "AND (%(area)s - %(area_percentage)s <= a.area AND a.area <= %(area)s + %(area_percentage)s) "
    results = db.execute_query(query,
                               params={'latitude': latitude,
                                       'longitude': longitude,
                                       'half_side': side / 2,
                                       'rooms': rooms,
                                       'area': area,
                                       'area_percentage': area / 5},
                               dict_cursor=True)
    return [dict(record) for record in results]
