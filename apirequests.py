import aiohttp
import logging

logger = logging.getLogger(f"CCCBot.{__name__}")

async def ccc_search(ctx, order):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://www.castingcall.club/api/v1/search?order_by={order}") as response:
            if response.status != 200:
                await ctx.send(f"CCC API returned a {response.status} error")
                logging.warning(f"CCC API returned a {response.status} error. Context: {ctx.message.content}")
                return
            response = await response.json()
            await session.close()
    return response

async def ccc_users(ctx, name, page_num):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://www.castingcall.club/api/v1/voicesearch?contains={name}") as response:
            if response.status != 200:
                await ctx.send(f"CCC API returned a {response.status} error")
                logging.warning(f"CCC API returend a {response.status} error. Context: {ctx.message.content}")
                return
            response = await response.json()
            await session.close()
    return response