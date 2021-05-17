import os
from concurrent import futures
import grequests
import grpc
from grpc_reflection.v1alpha import reflection

import service_pb2
import service_pb2_grpc


app_port = os.getenv('PORT_APP', 3000)
api_port = os.getenv('PORT_API', 4000)
api_url = f'http://slow_api:{api_port}/'
n = int(os.getenv('NUM_REQUESTS', 1))
cnt = [0]


class MyApp(service_pb2_grpc.MyAppServicer):
    def io_bound(
        self, request: service_pb2.MyAppRequest, context
    ) -> service_pb2.MyAppResponse:
        cnt[0] += 1
        reqs = []
        for _ in range(n):
            reqs.append(grequests.get(f'{api_url}?delay={request.delay}'))
        resps = [x.text for x in grequests.map(reqs)]
        return service_pb2.MyAppResponse(text=f'{cnt} {resps}')


def main():
    server = grpc.server(futures.ThreadPoolExecutor())
    reflection.enable_server_reflection(
        (service_pb2.DESCRIPTOR.services_by_name['MyApp'].full_name, ),
        server)
    app = MyApp()
    service_pb2_grpc.add_MyAppServicer_to_server(app, server)
    server.add_insecure_port(f'[::]:{app_port}')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    main()
