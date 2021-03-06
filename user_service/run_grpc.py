import time
from concurrent import futures

import click
import grpc

import server
from user_service_client.proto import authentication_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


@click.command()
@click.option('--port', default=5000)
@click.option('--max-workers', default=16)
def run(port, max_workers, grpc_interface='[::]'):
    thread_pool = futures.ThreadPoolExecutor(max_workers=max_workers)
    grpc_server = grpc.server(thread_pool=thread_pool)
    grpc_server.add_insecure_port(grpc_interface + ':' + str(port))

    authentication_pb2_grpc.add_AuthenticationServicer_to_server(server.AuthenticationServicer(),
                                                                 grpc_server)

    grpc_server.start()

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        grpc_server.stop(0)


if __name__ == '__main__':
    run()
