import asyncio
import aiohttp
import os

import requests
from fastapi import FastAPI


app = FastAPI()
FastAPI()


api_port = os.getenv('PORT_API', 4000)
api_url = f'http://slow_api:{api_port}/'

n = int(os.getenv('NUM_REQUESTS', 1))


cnt= [0]

async def async_get(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


@app.get('/')
async def index(delay: int = 1):
    try:
        cnt[0] += 1
        reqs = []
        for i in range(n):
            reqs.append(async_get(f'{api_url}?delay={delay}'))
        resps = await asyncio.gather(*reqs)
        return f'{cnt} {resps}'
    except Exception as e:
        print(e)
        raise e

