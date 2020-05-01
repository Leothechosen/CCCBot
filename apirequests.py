import aiohttp

async def ccc_search(ctx, order):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://www.castingcall.club/api/v1/search?order_by={order}") as response:
            if response.status != 200:
                await ctx.send(f"CCC API returned a {response.status} error")
                logging.warning(f"CCC API returned a {response.status} error. Order: {order}")
                return
            response = await response.json()
            await session.close()
    return response