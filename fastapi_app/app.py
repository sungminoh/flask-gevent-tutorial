from collections import defaultdict
import asyncio
import aiohttp
import os

import requests
from fastapi import FastAPI
import numpy as np


app = FastAPI()
FastAPI()


api_port = os.getenv('PORT_API', 4000)
api_url = f'http://slow_api:{api_port}/'

n = int(os.getenv('NUM_REQUESTS', 1))


count = defaultdict(int)


async def async_get(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


@app.get('/')
async def index():
    return 'ready'


@app.get('/io_bound')
async def io_bound(delay: int = 1):
    try:
        count['io_bound'] += 1
        reqs = []
        for i in range(n):
            reqs.append(async_get(f'{api_url}?delay={delay}'))
        resps = await asyncio.gather(*reqs)
        return f'[{count["io_bound"]}] {resps}'
    except Exception as e:
        print(e)
        raise e


def long_running(n):
    m = np.random.random((100, 100))
    for _ in range(n):
        m *= np.random.random((100, 100)) + np.random.random((100, 100))
    return m


@app.get('/cpu_bound')
async def cpu_bound(num: int = 1000):
    try:
        count['cpu_bound'] += 1
        return f'[{count["cpu_bound"]}] {long_running(num).shape}'
    except Exception as e:
        print(e)
        raise e
