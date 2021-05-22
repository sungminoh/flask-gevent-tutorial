from collections import defaultdict
import os

import grequests
from flask import Flask, request
import numpy as np


api_port = os.getenv('PORT_API', 4000)
api_url = f'http://slow_api:{api_port}/'
n = int(os.getenv('NUM_REQUESTS', 1))

count = defaultdict(int)

app = Flask(__name__)


@app.route('/')
def index():
    return 'ready'


@app.route('/io_bound')
def io_bound():
    count['io_bound'] += 1
    delay = int(request.args.get('delay') or 1)
    reqs = []
    for _ in range(n):
        reqs.append(grequests.get(f'{api_url}?delay={delay}'))
    resps = [x.text for x in grequests.map(reqs)]
    return f'[{count["io_bound"]}] {resps}', 200


def long_running(n):
    m = np.random.random((100, 100))
    for _ in range(n):
        m *= np.random.random((100, 100)) + np.random.random((100, 100))
    return m


@app.route('/cpu_bound')
def cpu_bound():
    count['cpu_bound'] += 1
    return f'[{count["cpu_bound"]}] {long_running(int(request.args.get("num") or 1000)).shape}', 200

