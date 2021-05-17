# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from grpc_app import service_pb2 as grpc__app_dot_service__pb2


class MyAppStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.io_bound = channel.unary_unary(
                '/MyApp/io_bound',
                request_serializer=grpc__app_dot_service__pb2.MyAppRequest.SerializeToString,
                response_deserializer=grpc__app_dot_service__pb2.MyAppResponse.FromString,
                )
        self.cpu_bound = channel.unary_unary(
                '/MyApp/cpu_bound',
                request_serializer=grpc__app_dot_service__pb2.MyAppRequest.SerializeToString,
                response_deserializer=grpc__app_dot_service__pb2.MyAppResponse.FromString,
                )


class MyAppServicer(object):
    """Missing associated documentation comment in .proto file."""

    def io_bound(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def cpu_bound(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MyAppServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'io_bound': grpc.unary_unary_rpc_method_handler(
                    servicer.io_bound,
                    request_deserializer=grpc__app_dot_service__pb2.MyAppRequest.FromString,
                    response_serializer=grpc__app_dot_service__pb2.MyAppResponse.SerializeToString,
            ),
            'cpu_bound': grpc.unary_unary_rpc_method_handler(
                    servicer.cpu_bound,
                    request_deserializer=grpc__app_dot_service__pb2.MyAppRequest.FromString,
                    response_serializer=grpc__app_dot_service__pb2.MyAppResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'MyApp', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class MyApp(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def io_bound(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/MyApp/io_bound',
            grpc__app_dot_service__pb2.MyAppRequest.SerializeToString,
            grpc__app_dot_service__pb2.MyAppResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def cpu_bound(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/MyApp/cpu_bound',
            grpc__app_dot_service__pb2.MyAppRequest.SerializeToString,
            grpc__app_dot_service__pb2.MyAppResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
