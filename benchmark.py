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
    parser.add_argument('protocol', choices=['http', 'grpc'])
    parser.add_argument('bound', choices=['io', 'cpu'])
    return parser.parse_args()


def curl(bound):
    s = time.time()
    try:
        response = requests.get(f'http://localhost:3000/{bound}_bound')
    except Exception as e:
        return time.time() - s, False
    return time.time() - s, response.status_code == 200


def call_grpc(stub, req, bound):
    s = time.time()
    try:
        if bound == 'io':
            response = stub.io_bound(req)
        elif bound == 'cpu':
            response = stub.cpu_bound(req)
    except Exception as e:
        return time.time() - s, False
    return time.time() - s, True


def run_grpc(pool, n, bound):
    channel =grpc.insecure_channel('localhost:3000')
    stub = service_pb2_grpc.MyAppStub(channel)
    req = service_pb2.MyAppRequest()
    s = time.time()
    elapsed = list(pool.map(
        call_grpc,
        (stub for _ in range(n)),
        (req for _ in range(n)),
        (bound for _ in range(n))
    ))
    total_elapsed = time.time() - s
    return total_elapsed, elapsed


def run_http(pool, n, bound):
    s = time.time()
    results = list(pool.map(curl, (bound for _ in range(n))))
    total_elapsed = time.time() - s
    return total_elapsed, results


def main():
    args = get_args()
    pool = futures.ThreadPoolExecutor(args.concurrency)
    if args.protocol == 'http':
        total_elapsed, results = run_http(pool, args.requests, args.bound)
    elif args.protocol == 'grpc':
        total_elapsed, results = run_grpc(pool, args.requests, args.bound)
    failure = len([result for result in results if not result[1]])
    elapsed = [result[0] for result in results if result[1]]
    print(f'Number of failure:    {failure}')
    print(f'Request per second:   {len(elapsed)/total_elapsed} [#/sec] (mean)')
    print(f'Time per request:     {1000*sum(elapsed)/len(elapsed)} [ms] (mean)')
    elapsed.sort()
    for i in range(5, 11):
        print('{:>2}0%   '.format(i) +  str(1000*elapsed[int(i/10*(len(elapsed)-1))]))


if __name__ == '__main__':
    main()


