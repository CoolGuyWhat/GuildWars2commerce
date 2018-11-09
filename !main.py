import asyncio
from aiohttp import ClientSession

async def fetch(url, session):
    async with session.get(url) as response:
        return await response.json()

async def connect(number):
    url = "https://api.guildwars2.com/v2/commerce/prices?page={}&page_size=200"
    id_url = "https://api.guildwars2.com/v2/items?ids="

    async with ClientSession() as session:
        tasks = []
        for i in range(number):
            task = asyncio.create_task(fetch(url.format(i), session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        
        item_ids = []

        for resp in responses:
            for res in resp:
                item_ids.append(str(res["id"]))

        tasks = []
        seperated_ids = [item_ids[x:x+200] for x in range(0, len(item_ids), 200)]
        for seperated_id in seperated_ids:
            url_id = ','.join(seperated_id)
            new_url = id_url + url_id
            task = asyncio.create_task(fetch(new_url, session))
            tasks.append(task)

        item_name = await asyncio.gather(*tasks)
        
        item_names = []
        for item in item_name:
            for ite in item:
                item_names.append(str(ite["name"]))
        print(item_names)
        

future = asyncio.ensure_future(connect(126)) 

loop = asyncio.get_event_loop()
loop.run_until_complete(future)