import os

import grequests
from flask import Flask, request

api_port = os.getenv('PORT_API', 4000)
api_url = f'http://slow_api:{api_port}/'
n = int(os.getenv('NUM_REQUESTS', 1))
cnt = [0]

app = Flask(__name__)

@app.route('/')
def index():
    cnt[0] += 1
    delay = int(request.args.get('delay') or 1)
    reqs = []
    for _ in range(n):
        reqs.append(grequests.get(f'{api_url}?delay={delay}'))
    resps = [x.text for x in grequests.map(reqs)]
    return f'{cnt} {resps}'

