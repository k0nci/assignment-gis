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


async def count_occurrence_in_region(country_id):
    query = """WITH region_occurrence AS (
                    SELECT crp.region_osm_id,
                           count(hl.name) as occurrence
                    FROM country_region_polygons crp
                    LEFT JOIN hurricane_lines hl
                        ON st_intersects(crp.region_geom, hl.way)
                    WHERE crp.country_osm_id = $1::bigint
                    GROUP BY crp.region_osm_id
               )
               SELECT cr.region_name,
                      ro.occurrence,
                      st_asgeojson(cr.region_geom) as geojson
               FROM region_occurrence ro
               JOIN country_region_polygons cr
                    ON ro.region_osm_id = cr.region_osm_id"""

    data = await database.fetch(query, country_id)

    if data is None:
        return []

    def parse(record):
        return to_geojson(
            region_name=record['region_name'],
            occurrence=record['occurrence'],
            geometry=loads(record['geojson'])
        )

    return [parse(x) for x in data]


async def count_occurrence_in_country(country_id):
    query = """SELECT cp.name, 
                      count(hl.name) as occurrence, 
                      st_asgeojson(st_multi(st_union(cp.geom))) as geojson
               FROM country_polygons cp
               LEFT JOIN hurricane_lines hl ON st_intersects(cp.geom, hl.way)
               WHERE cp.osm_id = $1::bigint
               GROUP BY cp.name"""

    data = await database.fetchone(query, country_id)

    if data is None:
        return {}
    return to_geojson(
        name=data['name'],
        occurrence=data['occurrence'],
        geometry=loads(data['geojson'])
    )
