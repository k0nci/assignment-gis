from quart.json import loads

import database


async def find_all():
    data = await database.fetch(
        """SELECT st_asgeojson(h_l.way) as geo_json 
        FROM hurricane_lines h_l"""
    )

    if data is None:
        return []
    return [loads(x['geo_json']) for x in data]
