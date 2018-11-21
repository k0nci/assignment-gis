from quart import current_app


async def fetch(query, *args):
    return await current_app.pool.fetch(query, *args)


async def fetchone(query, *args):
    return await current_app.pool.fetchrow(query, *args)
