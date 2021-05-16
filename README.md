# Python server deployment benchmark

Each request calls `slow_api` 10 times. `slow_api` takes 1 second.



* Sync (`grequests` is used to call `slow_api` concurrently)
  * Flask dev server
  * Flask dev server (threaded)
  * Flask + uwsgi
  * Flask + gunicorn
* Async
  * Flask + gevent (pywsgi)
  * Flask + gevent + uwsgi
  * Flask +gevent + gunicorn
  * FastAPI + uvicorn
  * FastAPI + uvicorn + gunicorn



## Sync

### Flask dev server

```sh
flask run --no-reload --without-threads --host 0.0.0.0 --port 3000
```

```
Requests per second:    0.94 [#/sec] (mean)
Time per request:       213078.233 [ms] (mean)
Time per request:       1065.391 [ms] (mean, across all concurrent requests)
```

### Flask dev server with thread

```sh
flask run --no-reload --with-threads --host 0.0.0.0 --port 3000
```

```
Requests per second:    30.19 [#/sec] (mean)
Time per request:       6624.230 [ms] (mean)
Time per request:       33.121 [ms] (mean, across all concurrent requests)

Percentage of the requests served within a certain time (ms)
  50%   5527
  66%   5720
  75%   6182
  80%   6481
  90%   6887
  95%   8693
  98%   9136
  99%   9485
 100%  12231 (longest request)
```

The next call returns `587` . Some are missing.



### Flask + uwsgi

#### 1 process * 50 threads

```sh
uwsgi --master \
  --workers 1 \
  --threads 50 \
  --protocol http \
  --socket 0.0.0.0:3000 \
  --module app:app
```

```
Requests per second:    19.53 [#/sec] (mean)
Time per request:       10242.165 [ms] (mean)
Time per request:       51.211 [ms] (mean, across all concurrent requests)

Percentage of the requests served within a certain time (ms)
  50%   6185
  66%   6371
  75%   6510
  80%   6605
  90%   7116
  95%  29605
  98%  29651
  99%  29661
 100%  29670 (longest request)
```

The next call returns `602` which is expected

#### 1 process * 200 threads

```sh
uwsgi --master \
  --workers 1 \
  --threads 200 \
  --protocol http \
  --socket 0.0.0.0:3000 \
  --module app:app
```

```
Requests per second:    19.43 [#/sec] (mean)
Time per request:       10295.817 [ms] (mean)
Time per request:       51.479 [ms] (mean, across all concurrent requests)

Percentage of the requests served within a certain time (ms)
  50%   9421
  66%  10916
  75%  11865
  80%  12430
  90%  13686
  95%  15293
  98%  16649
  99%  17224
 100%  18043 (longest request)
```

The next call returns `602` which is expected

#### 4 processes * 50 threads

```sh
uwsgi --master \
  --workers 4 \
  --threads 50 \
  --protocol http \
  --socket 0.0.0.0:3000 \
  --module app:app
```

```
Requests per second:    43.49 [#/sec] (mean)
Time per request:       4598.765 [ms] (mean)
Time per request:       22.994 [ms] (mean, across all concurrent requests)

Percentage of the requests served within a certain time (ms)
  50%   3979
  66%   4300
  75%   4569
  80%   4820
  90%   5324
  95%   5850
  98%   6190
  99%   6443
 100%   6888 (longest request)
```



### Flask + gunicorn

#### 1 process * 50 threads

```sh
gunicorn --workers 1 \
  --threads 50 \
  --bind 0.0.0.0:3000 \ 
  app:app
```

```
Requests per second:    25.50 [#/sec] (mean)
Time per request:       7842.762 [ms] (mean)
Time per request:       39.214 [ms] (mean, across all concurrent requests)

Percentage of the requests served within a certain time (ms)
  50%   7525
  66%   8130
  75%   8432
  80%   8619
  90%   8937
  95%   9144
  98%   9334
  99%   9480
 100%   9689 (longest request)
```

The next call returns `582`. Some are missing.

#### 1 process * 200 threads

```sh
gunicorn --workers 1 \
  --threads 200 \
  --bind 0.0.0.0:3000 \ 
  app:app
```

```
Requests per second:    32.71 [#/sec] (mean)
Time per request:       6114.812 [ms] (mean)
Time per request:       30.574 [ms] (mean, across all concurrent requests)

Percentage of the requests served within a certain time (ms)
  50%   5680
  66%   5977
  75%   6200
  80%   6343
  90%   6703
  95%   7060
  98%   7654
  99%   8931
 100%   9328 (longest request)
```

The next call returns `567` . Some are missing

#### 4 processes * 50 threads

```sh
gunicorn --workers 4 \
  --threads 50 \
  --bind 0.0.0.0:3000 \ 
  app:app
```

```
Requests per second:    52.88 [#/sec] (mean)
Time per request:       3781.952 [ms] (mean)
Time per request:       18.910 [ms] (mean, across all concurrent requests)

Percentage of the requests served within a certain time (ms)
  50%   3268
  66%   3651
  75%   3885
  80%   4133
  90%   4626
  95%   5007
  98%   5437
  99%   5568
 100%   6682 (longest request)
```



## Async

### Flask + gevent + uwsgi

#### 1 process * 2000 async cores

```sh
uwsgi --master \
  --single-interpreter \
  --workers 1 \
  --gevent 2000 \
  --protocol http \
  --socket 0.0.0.0:3000 \
  --module patched:app
```

```
Requests per second:    35.24 [#/sec] (mean)
Time per request:       5675.746 [ms] (mean)
Time per request:       28.379 [ms] (mean, across all concurrent requests)

Percentage of the requests served within a certain time (ms)
  50%   4190
  66%   5216
  75%   6510
  80%   7100
  90%   8166
  95%   8839
  98%  10256
  99%  10492
 100%  10592 (longest request)
```

The next call returns `602` which is expected.

#### 4 processes * 2000 async cores

```sh
uwsgi --master \
  --single-interpreter \
  --workers 4 \
  --gevent 2000 \
  --protocol http \
  --socket 0.0.0.0:3000 \
  --module patched:app
```

```
Requests per second:    61.26 [#/sec] (mean)
Time per request:       3264.934 [ms] (mean)
Time per request:       16.325 [ms] (mean, across all concurrent requests)

Percentage of the requests served within a certain time (ms)
  50%   2260
  66%   2545
  75%   2682
  80%   2841
  90%   3125
  95%   3428
  98%   3760
  99%   3981
 100%   4330 (longest request)
```



### Flask + gevent + gunicorn

#### 1 process

```sh
gunicorn --worker-class gevent \
  --workers 1 \
  --bind 0.0.0.0:3000 \ 
  patched:app
```

```
Requests per second:    36.78 [#/sec] (mean)
Time per request:       5438.161 [ms] (mean)
Time per request:       27.191 [ms] (mean, across all concurrent requests)

Percentage of the requests served within a certain time (ms)
  50%   4885
  66%   5549
  75%   5815
  80%   5893
  90%   6580
  95%   7908
  98%   8232
  99%   8258
 100%   8278 (longest request)
```

The next call returns `602` which is expected.

#### 4 processes

```sh
gunicorn --worker-class gevent \
  --workers 4 \
  --bind 0.0.0.0:3000 \ 
  patched:app
```

```
Requests per second:    76.37 [#/sec] (mean)
Time per request:       2618.685 [ms] (mean)
Time per request:       13.093 [ms] (mean, across all concurrent requests)

Percentage of the requests served within a certain time (ms)
  50%   1923
  66%   2204
  75%   2299
  80%   2453
  90%   2621
  95%   2755
  98%   2937
  99%   3008
 100%   3068 (longest request)
```



### FastAPI + uvicorn

#### 1 process

```sh
uvicorn --host 0.0.0.0 --port 3000 --workers 1 'app:app'
```

```
Requests per second:    65.18 [#/sec] (mean)
Time per request:       3068.454 [ms] (mean)
Time per request:       15.342 [ms] (mean, across all concurrent requests)

Percentage of the requests served within a certain time (ms)
  50%   1981
  66%   2221
  75%   2532
  80%   2637
  90%   3008
  95%   3747
  98%   3759
  99%   3762
 100%   3772 (longest request)
```

The next call returns `602` which is expected.

#### 4 processes

```sh
uvicorn --host 0.0.0.0 --port 3000 --workers 4 'app:app'
```

```
Requests per second:    78.07 [#/sec] (mean)
Time per request:       2561.828 [ms] (mean)
Time per request:       12.809 [ms] (mean, across all concurrent requests)

Percentage of the requests served within a certain time (ms)
  50%   1574
  66%   2039
  75%   2267
  80%   2318
  90%   2470
  95%   2575
  98%   2740
  99%   4369
 100%   4381 (longest request)
```



### FastAPI + uvicorn + gunicorn

#### 1 process

```sh
gunicorn --worker-class uvicorn.workers.UvicornWorker \
  --workers 1 \
  --bind "0.0.0.0:3000" \
  'app:app'
```

```
Requests per second:    72.04 [#/sec] (mean)
Time per request:       2776.132 [ms] (mean)
Time per request:       13.881 [ms] (mean, across all concurrent requests)

Percentage of the requests served within a certain time (ms)
  50%   2074
  66%   2236
  75%   2510
  80%   2648
  90%   2817
  95%   3159
  98%   3433
  99%   3854
 100%   3863 (longest request)
```

The next call returns `602` which is expected.

#### 4 processes

```sh
gunicorn --worker-class uvicorn.workers.UvicornWorker \
  --workers 4 \
  --bind "0.0.0.0:3000" \
  'app:app'
```

```
Requests per second:    85.53 [#/sec] (mean)
Time per request:       2338.386 [ms] (mean)
Time per request:       11.692 [ms] (mean, across all concurrent requests)

Percentage of the requests served within a certain time (ms)
  50%   1536
  66%   1857
  75%   2111
  80%   2158
  90%   2315
  95%   3370
  98%   5117
  99%   5235
 100%   5243 (longest request)
```

