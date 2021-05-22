from collections import defaultdict
import aiohttp
import asyncio
import os
import grpc.aio
from grpc_reflection.v1alpha import reflection
import numpy as np

import service_pb2
import service_pb2_grpc


app_port = os.getenv('PORT_APP', 3000)
api_port = os.getenv('PORT_API', 4000)
api_url = f'http://slow_api:{api_port}/'
n = int(os.getenv('NUM_REQUESTS', 1))

count = defaultdict(int)


def long_running(n):
    m = np.random.random((100, 100))
    for _ in range(n):
        m *= np.random.random((100, 100)) + np.random.random((100, 100))
    return m


async def async_get(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


class MyApp(service_pb2_grpc.MyAppServicer):
    async def index(
        self, request: service_pb2.MyAppRequest, context
    ) -> service_pb2.MyAppResponse:
        return service_pb2.MyAppResponse(text='ready')

    async def io_bound(
        self, request: service_pb2.MyAppRequest, context
    ) -> service_pb2.MyAppResponse:
        count['io_bound'] += 1
        reqs = []
        for i in range(n):
            reqs.append(async_get(f'{api_url}?delay={request.num or 10}'))
        resps = await asyncio.gather(*reqs)
        return service_pb2.MyAppResponse(text=f'[{count["io_bound"]}] {resps}')

    async def cpu_bound(
        self, request: service_pb2.MyAppRequest, context
    ) -> service_pb2.MyAppResponse:
        count['cpu_bound'] += 1
        result = long_running(request.num or 1000)
        return service_pb2.MyAppResponse(text=f'[{count["cpu_bound"]}] {result.shape}')


async def start():
    server = grpc.aio.server()
    reflection.enable_server_reflection(
        (service_pb2.DESCRIPTOR.services_by_name['MyApp'].full_name, ),
        server)
    app = MyApp()
    service_pb2_grpc.add_MyAppServicer_to_server(app, server)
    server.add_insecure_port(f'[::]:{app_port}')
    await server.start()
    await server.wait_for_termination()


def main():
    asyncio.run(start())


if __name__ == '__main__':
    main()
