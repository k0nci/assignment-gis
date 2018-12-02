CREATE MATERIALIZED VIEW hurricane_lines AS
SELECT h.id,
       hp.hurricane_id,
       h.name,
       min(hp.timestamp) as start_date,
       max(hp.timestamp) as end_date,
       st_makeline(hp.way) as way
FROM (SELECT * FROM hurricane_points ORDER BY hurricane_id, timestamp) hp
       JOIN hurricanes h ON h.id = hp.hurricane_id
GROUP BY h.id, hp.hurricane_id, h.name
HAVING count(*) > 1;

CREATE INDEX hurricane_lines_way_i
ON hurricane_lines
USING gist(way);

CREATE INDEX h_l_start_date_year_i
ON hurricane_lines(extract(year from start_date));

CREATE MATERIALIZED VIEW country_polygons AS
SELECT p.name,
       p.osm_id,
       st_multi(st_union(p.way)) as geom
FROM planet_osm_polygon p
WHERE p.boundary = 'administrative'
  AND p.admin_level = '2'
GROUP BY p.name, p.osm_id;

CREATE MATERIALIZED VIEW country_region_polygons AS
  WITH country_region AS (SELECT cp.name                   as country_name,
                                 cp.osm_id                 as country_osm_id,
                                 p.name                    as region_name,
                                 p.osm_id                  as region_osm_id,
                                 st_multi(st_union(p.way)) as region_geom
                          FROM country_polygons cp
                                 JOIN planet_osm_polygon p
                                      ON st_intersects(cp.geom, p.way)
                          WHERE p.boundary = 'administrative'
                            AND p.admin_level = '4'
                          GROUP BY cp.name, cp.osm_id, p.name, p.osm_id),
    region_area AS (SELECT cr.region_osm_id,
                           max(st_area(
                               st_intersection(cp.geom, cr.region_geom)::geography)) as max_area
                    FROM country_region cr
                           JOIN country_polygons cp
                                ON cp.name = cr.country_name
                    GROUP BY cr.region_osm_id)
    SELECT cr.country_name,
           cr.country_osm_id,
           cr.region_name,
           cr.region_osm_id,
           cr.region_geom,
           ra.max_area as region_area
    FROM country_region cr
           JOIN country_polygons cp ON cp.name = cr.country_name
           JOIN region_area ra ON cr.region_osm_id = ra.region_osm_id
    WHERE st_area(st_intersection(cp.geom, cr.region_geom)::geography) =
          ra.max_area
      AND ra.max_area > 0;

-- for find_dwithin query
CREATE INDEX hurricane_lines_way_geography_i
  ON hurricane_lines
    USING gist (geography(way));

-- for count_occurrence_in_region
CREATE INDEX c_r_p_country_osm_id_i
  ON country_region_polygons (country_osm_id);

CREATE INDEX c_r_p_region_osm_id_i
  ON country_region_polygons (region_osm_id);

-- for count_occurrence_in_country
CREATE INDEX c_p_osm_id_name
  ON country_polygons (osm_id, name);


CREATE MATERIALIZED VIEW hurricane_part_lines AS
  WITH hurricane_next_point as (
    SELECT hp.id,
           hp.hurricane_id,
           hp.status,
           hp.way                                                         as point,
           lead(hp.way)
                OVER (PARTITION BY hp.hurricane_id ORDER BY hp.timestamp) as next_point
    FROM hurricane_points hp)
    SELECT hpl.id,
           hpl.hurricane_id,
           hpl.status,
           st_makeline(hpl.point, hpl.next_point) as geom
    FROM hurricane_next_point hpl
    WHERE hpl.next_point NOTNULL;


CREATE INDEX h_p_l_hurricane_id_i
  ON hurricane_part_lines (hurricane_id);

CREATE INDEX h_l_hurricane_id_i
ON hurricane_lines(hurricane_id);




