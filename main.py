"""
Proprietary License

Copyright 2024 Bueezi™
All Rights Reserved.

This software is licensed under the Proprietary License. Unauthorized copying, modification, distribution, or use
of this software is strictly prohibited. For full license details, see the LICENSE file in this repository.
"""

import asyncio, json, random
from src.unlock_cookie import Unlock_Cookies
with open("new_cookies.txt", "r") as f:
    if "_" in f.read(): Unlock_Cookies()
from src.fetch import Fetch, Status
from src.webhook import Send_Webhook
from src.get_cookie import Get_Cookie
from src.tor import Make_Proxies
from src.get_ids import Get_IDs

proxy_start_port = 50_000 # if tor won't launch changing this may help, try 9080 or 15000
"""proxies = None 
with open("proxies.txt", "r") as f: # Uncomment to use proxies from proxies.txt
    proxies = f.readlines()"""
config = None
with open("config.json", "r") as f:
    config = json.load(f)
closed_list = None
with open("src/closed.txt", "r") as f:
    closed_list = f.readlines()
    closed_list = [int(_.replace("\n", "")) for _ in closed_list]

def AddClosed(ID):
    closed_list.append(ID)
    with open("src/closed.txt", "a") as f:
        f.write(str(ID)+ "\n")

async def Thread(n):
    await asyncio.sleep(n/4) # gradually increase the amount of active threads
    proxy = "http://127.0.0.1:"+str(proxy_start_port+n+1)
    make_closed_list_mode = True # Change this to False one's the closed.txt id list is done making
    while 1:
        #proxy = f"http://{random.choice(proxies)}" # Uncomment to use proxies from proxies.txt
        url = f"https://groups.roblox.com/v2/groups?groupIds={Get_IDs()}"
        data, error = await Fetch(url, Get_Cookie(), proxy)
        if error: continue
        for group in data["data"]:
            if group["owner"] is None:
                if group["id"] not in closed_list:
                    if make_closed_list_mode: 
                        AddClosed(group["id"])
                    data, error = await Fetch(f"https://groups.roblox.com/v1/groups/{group['id']}", Get_Cookie(), proxy)
                    #data, error = await Fetch(f"https://groups.roblox.com/v1/groups/{group['id']}") # Use this one one's Closed.txt done making
                    if error: continue
                    if "isLocked" not in data and data["publicEntryAllowed"] == True:
                        print(f"True Ownerless found : {str(group['id'])}")
                        message = f"<@{config['discord_userID']}> https://www.roblox.com/groups/{str(group['id'])}"
                        await Send_Webhook(config["webhook_url"] ,message)
                        with open("src/logs.txt", "a") as f:
                            f.write(f"Found Ownerless group : {str(group['id'])}\n")
                    elif not make_closed_list_mode:
                        AddClosed(group["id"])

async def main():
    thread_amount=100 # Changing this may cause Tor to crash, a good rule of thumb would be 100 threads per 500k CPM so if u do around 750k CPM this should be no more than 150
    Make_Proxies(thread_amount, proxy_start_port)
    tasks = [asyncio.create_task(Thread(_)) for _ in range(thread_amount)]
    tasks.append(asyncio.create_task(Status()))
    await asyncio.gather(*tasks)

asyncio.run(main())