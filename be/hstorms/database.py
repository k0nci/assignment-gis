import re
from quart import current_app as app


async def fetch(query: str, *args):
    app.logger.debug('fetch(query={}, args={})'
                     .format(re.sub(r'\n\s*', ' ', query), args))
    return await app.pool.fetch(query, *args)


async def fetchone(query, *args):
    app.logger.debug('fetchone(query={}, args={})'
                     .format(re.sub(r'\n\s*', ' ', query), args))
    return await app.pool.fetchrow(query, *args)
