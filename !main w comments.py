# https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html
# https://aiohttp.readthedocs.io/en/stable/index.html
import asyncio
from aiohttp import ClientSession

# This function opens a WebSession with the parsed url !and! session from the
# connect function. This way its only opening 1 web session.
# Then returns the JSON content. 
async def fetch(url, session):
    # Opens the session with the parased session and url and opens it as 'response'.
    async with session.get(url) as response:
        # Returns the response from the url as a JSON object.
        # https://aiohttp.readthedocs.io/en/stable/client_reference.html#aiohttp.ClientResponse.json
        return await response.json()

# Creates the Main function to execute on the Async loop
async def connect(number):
    # Setup urls as strings with dyname parts to be manipulated later
    url = "https://api.guildwars2.com/v2/commerce/prices?page={}&page_size=200"
    id_url = "https://api.guildwars2.com/v2/items?ids="

    async with ClientSession() as session: # Opens the session
        tasks = [] # Opens an empty list
        # For each number in the range specified in the Future variable
        for i in range(number):
            # Creates a task using the function Fetch with the URL and formats each number
            # in range into the url and creates a task for each in the tasks list.
            # Also for each session its only using the 1 ClientSession so we're not opening
            # potentially 100's of connection threads only the 1.
            task = asyncio.create_task(fetch(url.format(i), session))
            # Appends each task it creates to the list into the tasks list
            tasks.append(task)
        # The gather function runs all the tasks in the list. 
        responses = await asyncio.gather(*tasks)
        # Creates a new list for future processing.

        item_ids = []

        # Because the returned reponse from the Gather task is listed Json we need to drill down 2 levels.
        for resp in responses:
            for res in resp:
                # This then pulls the item ID number out of the json and appends it to the end of the item_ids list.
                item_ids.append(str(res["id"]))
        # Empties the task list for the for each loop below
        tasks = []
        # https://stackoverflow.com/questions/15890743/how-can-you-split-a-list-every-x-elements-and-add-those-x-amount-of-elements-to
        # Seperates the item_ids list into blocks of 200 for the 
        # I don't really know exactly how this works
        seperated_ids = [item_ids[x:x+200] for x in range(0, len(item_ids), 200)]
        for seperated_id in seperated_ids:
            # Creates a string joining each object in the seperated_id variable with the ,
            url_id = ','.join(seperated_id)
            # Joins the 2 strings together making the final url.
            new_url = id_url + url_id
            # Creates a new task for each chuck of 200 ids in the seperated_ids list with the final url
            task = asyncio.create_task(fetch(new_url, session))
            # Appends each task it creates to the list into the tasks list
            tasks.append(task)

        # Runs all the newly created tasks.
        item_name = await asyncio.gather(*tasks)

        # Creates a new Empty list
        item_names = []
        # For each item in the new task responses append the "name" value to the newly created list
        for item in item_name:
            for ite in item:
                item_names.append(str(ite["name"]))

        print(item_names)

future = asyncio.ensure_future(connect(1))

loop = asyncio.get_event_loop()
loop.run_until_complete(future)