from quart.json import loads

import database


async def find_closest(point):
    data = await database.fetchone(
        """WITH line_distance AS 
                (SELECT hl.way as line, st_distance(p.way, hl.way::geography) as distance
                FROM (SELECT st_setsrid(st_point($1, $2), 4326)::geography as way) p
                CROSS JOIN hurricane_lines hl)
           SELECT st_asgeojson(ld.line) as geojson
           FROM line_distance ld
           WHERE ld.distance = (SELECT min(distance) FROM line_distance)""",
        point['lon'],
        point['lat']
    )

    if data is None:
        return []
    return loads(data['geojson'])
