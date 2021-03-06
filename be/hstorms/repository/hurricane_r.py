from collections import defaultdict

from util import to_geojson, to_geojson_collection
import database


async def find_closest(point, year=None):
    if year:
        query = """WITH point AS (
                      SELECT st_setsrid(st_point($1, $2), 4326)::geography as way),
                         line_distance AS (
                      SELECT hl.hurricane_id,
                             st_distance(p.way, hl.way::geography) as distance
                      FROM hurricane_lines hl
                      CROSS JOIN point p
                      WHERE extract(year from hl.start_date) = $3),
                         min_distance_id AS (
                           SELECT ld1.hurricane_id,
                                  ld1.distance
                           FROM line_distance ld1
                           WHERE distance = (SELECT min(ld2.distance) FROM line_distance ld2))
                    SELECT hpl.hurricane_id,
                           h.name,
                           hpl.status,
                           md.distance as min_distance,
                           st_asgeojson(hpl.geom) as geojson
                    FROM hurricane_part_lines hpl
                    JOIN min_distance_id md ON md.hurricane_id = hpl.hurricane_id
                    JOIN hurricanes h ON h.id = hpl.hurricane_id"""

        data = await database.fetch(query, point['lon'], point['lat'], year)
    else:
        query = """WITH point AS (
                      SELECT st_setsrid(st_point($1, $2), 4326)::geography as way),
                         line_distance AS (
                      SELECT hl.hurricane_id,
                             st_distance(p.way, hl.way::geography) as distance
                      FROM hurricane_lines hl
                      CROSS JOIN point p),
                         min_distance_id AS (
                           SELECT ld1.hurricane_id,
                                  ld1.distance
                           FROM line_distance ld1
                           WHERE distance = (SELECT min(ld2.distance) FROM line_distance ld2))
                    SELECT hpl.hurricane_id,
                           h.name,
                           hpl.status,
                           md.distance as min_distance,
                           st_asgeojson(hpl.geom) as geojson
                    FROM hurricane_part_lines hpl
                    JOIN min_distance_id md ON md.hurricane_id = hpl.hurricane_id
                    JOIN hurricanes h ON h.id = hpl.hurricane_id"""

        data = await database.fetch(query, point['lon'], point['lat'])

    features = [to_geojson(status=x['status'],
                           geometry=x['geojson'],
                           name=x['name'],
                           hurricaneId=x['hurricane_id'],
                           minDistance=x['min_distance'])
                for x in data]

    return to_geojson_collection(features, name=data[0]['name'],
                                 hurricaneId=data[0]['hurricane_id'])


async def find_dwithin(point, distance, year=None):
    if year:
        query = """WITH point AS (
                      SELECT st_setsrid(st_point($1, $2), 4326)::geography way),
                         in_distance AS (
                           SELECT hl.hurricane_id
                           FROM hurricane_lines hl
                           CROSS JOIN point p
                           WHERE st_dwithin(hl.way::geography,
                                            p.way,
                                            $3)
                              AND extract(year from hl.start_date) = $4)
                    SELECT hpl.hurricane_id,
                           h.name,
                           hpl.status,
                           min(st_distance(p.way, hpl.geom::geography)) 
                                OVER (PARTITION BY hpl.hurricane_id) as min_distance,
                           st_asgeojson(hpl.geom)                  as geojson
                    FROM hurricane_part_lines hpl
                    JOIN in_distance i ON i.hurricane_id = hpl.hurricane_id
                    JOIN hurricanes h ON h.id = hpl.hurricane_id
                    CROSS JOIN point p"""

        data = await database.fetch(query,
                                    point['lon'], point['lat'],
                                    distance, year)

    else:
        query = """WITH point AS (
                      SELECT st_setsrid(st_point($1, $2), 4326)::geography way),
                         in_distance AS (
                           SELECT hl.hurricane_id
                           FROM hurricane_lines hl
                           CROSS JOIN point p
                           WHERE st_dwithin(hl.way::geography,
                                            p.way,
                                            $3))
                    SELECT hpl.hurricane_id,
                           h.name,
                           hpl.status,
                           min(st_distance(p.way, hpl.geom::geography)) 
                                OVER (PARTITION BY hpl.hurricane_id) as min_distance,
                           st_asgeojson(hpl.geom)                  as geojson
                    FROM hurricane_part_lines hpl
                    JOIN in_distance i ON i.hurricane_id = hpl.hurricane_id
                    JOIN hurricanes h ON h.id = hpl.hurricane_id
                    CROSS JOIN point p"""

        data = await database.fetch(query,
                                    point['lon'], point['lat'], distance)

    grouped = defaultdict(list)
    for x in data:
        hurricane_id = x['hurricane_id']
        feature = to_geojson(
            hurricaneId=hurricane_id,
            name=x['name'],
            status=x['status'],
            geometry=x['geojson'],
            minDistance=x['min_distance']
        )
        grouped[hurricane_id].append(feature)

    return [to_geojson_collection(x, name=x[0]['properties']['name'],
                                  hurricaneId=x[0]['properties']['hurricaneId'])
            for x in grouped.values()]


async def count_occurrence_in_region(country_id):
    query = """WITH region_occurrence AS (
                    SELECT crp.region_osm_id,
                           count(hl.id) as occurrence
                    FROM country_region_polygons crp
                    LEFT JOIN hurricane_lines hl
                        ON st_intersects(crp.region_geom, hl.way)
                    WHERE crp.country_osm_id = $1::bigint
                    GROUP BY crp.region_osm_id
               )
               SELECT cr.country_name,
                      cr.region_name,
                      cr.region_area,
                      ro.occurrence,
                      st_asgeojson(cr.region_geom) as geojson
               FROM region_occurrence ro
               JOIN country_region_polygons cr
                    ON ro.region_osm_id = cr.region_osm_id"""

    data = await database.fetch(query, country_id)

    if not data:
        return to_geojson_collection([])

    def parse(record):
        return to_geojson(
            regionName=record['region_name'],
            area=record['region_area'],
            occurrence=record['occurrence'],
            geometry=record['geojson']
        )

    return to_geojson_collection([parse(x) for x in data],
                                 countryName=data[0]['country_name'])


async def count_occurrence_in_country(country_id):
    query = """WITH occurrence AS (
                  SELECT cp.osm_id,
                         count(hl.id) as cnt
                  FROM country_polygons cp
                  LEFT JOIN hurricane_lines hl ON st_intersects(cp.geom, hl.way)
                  WHERE cp.osm_id = $1::bigint
                  GROUP BY cp.osm_id
                )
                SELECT cp.name as country_name,
                       st_area(cp.geom::geography) as country_area,
                       o.cnt as occurrence,
                       st_asgeojson(cp.geom) as geojson
                FROM country_polygons cp
                JOIN occurrence o ON o.osm_id = cp.osm_id;"""

    data = await database.fetchone(query, country_id)

    if data is None:
        return to_geojson({})

    return to_geojson(
        countryName=data['country_name'],
        area=data['country_area'],
        occurrence=data['occurrence'],
        geometry=data['geojson']
    )


async def get_hurricane_info(hurricane_id):
    query = """SELECT hl.hurricane_id,
                      hl.name,
                      hl.start_date,
                      hl.end_date,
                      st_length(hl.way::geography) as length
               FROM hurricane_lines hl
               WHERE hl.hurricane_id = $1"""

    data = await database.fetchone(query, hurricane_id)

    if data is None:
        return {}
    return {
        'hurricaneId': data['hurricane_id'],
        'hurricaneLength': data['length'],
        'name': data['name'],
        'startDate': data['start_date'],
        'endDate': data['end_date']
    }
