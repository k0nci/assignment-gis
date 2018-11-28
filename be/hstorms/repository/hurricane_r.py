from quart.json import loads
from collections import defaultdict

from util import to_geojson, to_geojson_collection
import database


async def find_closest(point):
    query = """WITH line_distance AS (
                  SELECT hl.hurricane_id,
                         st_distance(p.way, hl.way::geography) as distance
                  FROM hurricane_lines hl
                         CROSS JOIN (SELECT st_setsrid(st_point($1, $2), 4326)::geography as way) p),
                     min_distance_id AS (
                       SELECT ld1.hurricane_id
                       FROM line_distance ld1
                       WHERE distance = (SELECT min(ld2.distance) FROM line_distance ld2))
                SELECT hpl.hurricane_id,
                       h.name,
                       hpl.status,
                       st_asgeojson(geom) as geojson
                FROM hurricane_part_lines hpl
                JOIN min_distance_id md ON md.hurricane_id = hpl.hurricane_id
                JOIN hurricanes h ON h.id = hpl.hurricane_id"""

    data = await database.fetch(query, point['lon'], point['lat'])

    features = [to_geojson(status=x['status'], geometry=loads(x['geojson']),
                           name=x['name'], hurricaneId='hurricane_id')
                for x in data]
    return to_geojson_collection(features, name=data[0]['name'],
                                 hurricaneId=data[0]['hurricane_id'])


async def find_dwithin(point, distance):
    query = """WITH in_distance AS (
                  SELECT hl.hurricane_id
                  FROM hurricane_lines hl
                  WHERE st_dwithin(hl.way::geography,
                                   st_setsrid(st_point($1, $2), 4326)::geography,
                                   $3))
                SELECT hpl.hurricane_id,
                       h.name,
                       hpl.status, 
                       st_asgeojson(hpl.geom) as geojson
                FROM hurricane_part_lines hpl
                JOIN in_distance i ON i.hurricane_id = hpl.hurricane_id
                JOIN hurricanes h ON h.id = hpl.hurricane_id"""

    data = await database.fetch(query, point['lon'], point['lat'], distance)

    grouped = defaultdict(list)
    for x in data:
        hurricane_id = x['hurricane_id']
        feature = to_geojson(
            hurricaneId=hurricane_id,
            name=x['name'],
            status=x['status'],
            geometry=loads(x['geojson'])
        )
        grouped[hurricane_id].append(feature)

    return [to_geojson_collection(x, name=x[0]['properties']['name'],
                                  hurricaneId=x[0]['properties']['hurricaneId'])
            for x in grouped.values()]


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
