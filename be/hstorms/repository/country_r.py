import hstorms.database as db


async def find_countries():
    query = """SELECT cp.name, cp.osm_id
               FROM country_polygons cp"""
    data = await db.fetch(query)

    if not data:
        return []

    def parse_country(country):
        return {
            'text': country['name'],
            'value': country['osm_id']
        }
    return [parse_country(x) for x in data]
