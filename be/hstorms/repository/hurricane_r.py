from quart.json import loads

from util import to_geojson
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
    return to_geojson(geometry=loads(data['geojson']))


async def find_dwithin(point, distance):
    query = """SELECT st_asgeojson(hl.way) as geojson
               FROM hurricane_lines hl
               WHERE st_dwithin(hl.way::geography,
                                st_setsrid(st_point($1, $2), 4326)::geography,
                                $3)"""

    data = await database.fetch(query, point['lon'], point['lat'], distance)

    if data is None:
        return []
    return [to_geojson(geometry=loads(x['geojson'])) for x in data]


async def count_occurrence_in_region(country):
    query = """SELECT p.name, 
                      count(*) as occurrence, 
                      st_asgeojson(st_multi(st_union(p.way))) as geojson
               FROM country_polygons cp
               JOIN planet_osm_polygon p ON st_within(p.way, cp.geometry)
               JOIN hurricane_lines hl ON st_intersects(p.way, hl.way)
               WHERE cp.ids = $1::bigint[]
                 AND p.boundary = 'administrative'
                 AND p.admin_level = '4'
               GROUP BY p.name"""

    data = await database.fetch(query, country)

    if data is None:
        return []

    def parse(record):
        return to_geojson(
            name=record['name'],
            occurrence=record['occurrence'],
            geometry=loads(record['geojson'])
        )

    return [parse(x) for x in data]


async def count_occurrence_in_country(country):
    query = """SELECT cp.name, 
                      count(*) as occurrence, 
                      st_asgeojson(st_multi(st_union(cp.geometry))) as geojson
               FROM country_polygons cp
               JOIN hurricane_lines hl ON st_intersects(cp.geometry, hl.way)
               WHERE cp.ids = $1::bigint[]
               GROUP BY cp.name"""

    data = await database.fetchone(query, country)

    if data is None:
        return {}
    return to_geojson(
        name=data['name'],
        occurrence=data['occurrence'],
        geometry=loads(data['geojson'])
    )
