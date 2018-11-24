from quart.json import loads

import database


async def find_closest(point):
    query = """WITH line_distance AS
                (SELECT hl.way as line, 
                        st_distance(p.way::geography, hl.way::geography) as distance
                FROM hurricane_lines hl
                CROSS JOIN (SELECT st_setsrid(st_point($1, $2), 4326) as way) p)
           SELECT st_asgeojson(ld.line) as geojson
           FROM line_distance ld
           WHERE ld.distance = (SELECT min(distance) FROM line_distance)"""

    data = await database.fetchone(query, point['lon'], point['lat'])

    if data is None:
        return {}
    return loads(data['geojson'])


async def find_dwithin(point, distance):
    query = """SELECT st_asgeojson(hl.way) as geojson
               FROM hurricane_lines hl
               WHERE st_dwithin(hl.way::geography,
                                st_setsrid(st_point($1, $2), 4326)::geography,
                                $3)"""

    data = await database.fetch(query, point['lon'], point['lat'], distance)

    if data is None:
        return []
    return [loads(x['geojson']) for x in data]
