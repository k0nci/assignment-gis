import database


async def find_countries():
    query = """SELECT cp.name, cp.ids
               FROM country_polygons cp"""
    data = await database.fetch(query)

    if data is None:
        return []

    def parse_country(country):
        return {
            'name': country['name'],
            'ids': country['ids']
        }
    return [parse_country(x) for x in data]
