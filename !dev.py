import asyncio
from aiohttp import ClientSession
import json

async def fetch(url, session):
    async with session.get(url) as response:
        return await response.json()

async def connect(number):
    url = "https://api.guildwars2.com/v2/commerce/prices?page={}&page_size=25"
    id_url = "https://api.guildwars2.com/v2/items?ids="

    async with ClientSession() as session:
        tasks = []
        for i in range(number):
            task = asyncio.create_task(fetch(url.format(i), session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)

        each_item = []
        # Getting all the items in from the Respsonse into the List
        # For each Json Object put it into a list # {'id': 24, 'whitelisted': False, 'buys': {'quantity': 46864, 'unit_price': 179}, 'sells': {'quantity': 57059, 'unit_price': 324}}
        for value in responses:
            for i in range(25):
                each_item.append(value[i])
                print(value[i])
        
        item_ids = []
        # Get the ID for each item from the list above and appends it into a list
        for resp in responses:
            for res in resp:
                item_ids.append(str(res["id"]))

        tasks = []
        # Creates a new Task list for another Connection to shorten the Request load
        # items?ids=1,2,3,...,199,200
        seperated_ids = [item_ids[x:x+200] for x in range(0, len(item_ids), 200)]
        for seperated_id in seperated_ids:
            url_id = ','.join(seperated_id)
            new_url = id_url + url_id
            task = asyncio.create_task(fetch(new_url, session))
            tasks.append(task)

        item_name = await asyncio.gather(*tasks)
        
        item_names = [] # Each item name # Empty List
        # For each item in the new request get the item name from the response
        # And put it into the new empty List
        for item in item_name:
            for ite in item:
                item_names.append(str(ite["name"]))
        print(item_names)

        
        


future = asyncio.ensure_future(connect(1)) 

loop = asyncio.get_event_loop()
loop.run_until_complete(future)