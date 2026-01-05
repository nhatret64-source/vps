import asyncio, aiohttp

async def Send_Webhook(webhook_url, message):
    async with aiohttp.ClientSession() as session:
        payload = {"content": message}
        async with session.post(webhook_url, json=payload) as response:
            if response.status == 204:
                print("Message sent successfully!")
            else:
                print(f"Failed to send message. HTTP Status: {response.status}")