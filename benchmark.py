#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2021 sungminoh <smoh2044@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""
import subprocess
import os
import time
import argparse
import requests
from concurrent import futures
import grpc
from grpc_app import service_pb2_grpc
from grpc_app import service_pb2


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--requests', type=int, help='Number of requests to perform')
    parser.add_argument('-c', '--concurrency', type=int, help='Number of multiple requests to make at a time')
    parser.add_argument('protocol')
    return parser.parse_args()


def curl(dummy):
    s = time.time()
    requests.get('http://localhost:3000')
    return time.time() - s


def call_grpc(stub, req):
    s = time.time()
    response = stub.call(req)
    return time.time() - s


def run_grpc(pool, n):
    channel =grpc.insecure_channel('localhost:3000')
    stub = service_pb2_grpc.MyAppStub(channel)
    req = service_pb2.MyAppRequest(delay=1)
    s = time.time()
    elapsed = list(pool.map(call_grpc,
                            (stub for _ in range(n)),
                            (req for _ in range(n))))
    total_elapsed = time.time() - s
    return total_elapsed, elapsed

def run_http(pool, n):
    s = time.time()
    elapsed = list(pool.map(curl, (_ for _ in range(n))))
    total_elapsed = time.time() - s
    return total_elapsed, elapsed


def main():
    args = get_args()
    pool = futures.ThreadPoolExecutor(args.concurrency)
    if args.protocol == 'grpc':
        total_elapsed, elapsed = run_grpc(pool, args.requests)
    else:
        total_elapsed, elapsed = run_http(pool, args.requests)
    print(f'Request per second:   {len(elapsed)/total_elapsed} [#/sec] (mean)')
    print(f'Time per request:     {1000*sum(elapsed)/len(elapsed)} [ms] (mean)')
    elapsed.sort()
    for i in range(5, 11):
        print('{:>2}0%   '.format(i) +  str(1000*elapsed[int(i/10*(len(elapsed)-1))]))


if __name__ == '__main__':
    main()


