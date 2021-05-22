# Python server deployment benchmark

Each request calls `slow_api` 10 times. `slow_api` takes 1 second.



* Sync (`grequests` is used to call `slow_api` concurrently)
  * Flask dev server
  * Flask dev server with thread
  * Flask + uwsgi
  * Flask + gunicorn
  * grpc
* Async
  * Flask + gevent pywsgi (not included)
  * Flask + gevent + uwsgi
  * Flask +gevent + gunicorn
  * FastAPI + uvicorn
  * FastAPI + uvicorn + gunicorn
  * async grpc



## Sync

### Flask dev server

* Run: 

```shell
./run.sh sync-devserver io
```

```shell
flask run --no-reload --without-threads --host 0.0.0.0 --port 3000
```

```
Number of failure:    0
Request per second:   0.9738661956536023 [#/sec] (mean)
Time per request:     8731.268326441446 [ms] (mean)
 50%   10258.019208908081
 60%   10262.205839157104
 70%   10263.682126998901
 80%   10264.742851257324
 90%   10267.912864685059
100%   10287.858963012695
```

### Flask dev server with thread

* Run:

```shell
./run.sh sync-devserver-threaded io
```

```shell
flask run --no-reload --with-threads --host 0.0.0.0 --port 3000
```

```
Number of failure:    2
Request per second:   33.49386789353458 [#/sec] (mean)
Time per request:     2565.9279127248983 [ms] (mean)
 50%   2635.741949081421
 60%   2698.6732482910156
 70%   2758.758068084717
 80%   2868.894100189209
 90%   2974.337100982666
100%   3628.8628578186035
```



### Flask + uwsgi

* Run:

```shell
./run.sh sync-uwsgi io
```

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
Number of failure:    0
Request per second:   25.164941213862217 [#/sec] (mean)
Time per request:     3543.993002573649 [ms] (mean)
 50%   3811.6958141326904
 60%   3893.864154815674
 70%   3981.9493293762207
 80%   4061.771869659424
 90%   4250.969171524048
100%   4641.457796096802
```

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
Number of failure:    0
Request per second:   32.887102697864236 [#/sec] (mean)
Time per request:     2919.0240621566772 [ms] (mean)
 50%   2811.6679191589355
 60%   2928.098678588867
 70%   3173.66099357605
 80%   3366.018772125244
 90%   3848.794937133789
100%   5784.557819366455
```

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
Number of failure:    0
Request per second:   47.57190655682544 [#/sec] (mean)
Time per request:     1899.703250726064 [ms] (mean)
 50%   1847.8820323944092
 60%   1958.4388732910156
 70%   2148.693084716797
 80%   2373.0828762054443
 90%   2561.779022216797
100%   3129.5759677886963
```



### Flask + gunicorn

* Run:

```shell
./run.sh sync-gunicorn io
```

#### 1 process * 50 threads

```sh
gunicorn --workers 1 \
  --threads 50 \
  --bind 0.0.0.0:3000 \ 
  app:app
```

```
Number of failure:    3
Request per second:   28.51387087470644 [#/sec] (mean)
Time per request:     2964.7223548054294 [ms] (mean)
 50%   3042.6571369171143
 60%   3241.5568828582764
 70%   3399.2671966552734
 80%   3502.7129650115967
 90%   3625.8809566497803
100%   3863.651990890503
```

#### 1 process * 200 threads

```sh
gunicorn --workers 1 \
  --threads 200 \
  --bind 0.0.0.0:3000 \ 
  app:app
```

```
Number of failure:    3
Request per second:   32.56294067145921 [#/sec] (mean)
Time per request:     2755.5162970867223 [ms] (mean)
 50%   2793.282985687256
 60%   2879.5201778411865
 70%   2996.006965637207
 80%   3117.2468662261963
 90%   3375.765323638916
100%   4289.799928665161
```

#### 4 processes * 50 threads

```sh
gunicorn --workers 4 \
  --threads 50 \
  --bind 0.0.0.0:3000 \ 
  app:app
```

```
Number of failure:    26
Request per second:   50.89812030173422 [#/sec] (mean)
Time per request:     1582.2264800106523 [ms] (mean)
 50%   1597.090244293213
 60%   1684.3070983886719
 70%   1788.4752750396729
 80%   1903.5348892211914
 90%   2006.2541961669922
100%   2586.9359970092773
```



### gRPC 

* Run

```shell
./run.sh sync-grpc io
```

```sh
python app.py
```

```
Request per second:   1.1788415990370467 [#/sec] (mean)
Time per request:     72195.79920609792 [ms] (mean)
 50%   81456.04300498962
 60%   81555.6948184967
 70%   82072.97587394714
 80%   88640.5439376831
 90%   90418.27392578125
100%   91980.67808151245
```





## Async

### Flask + gevent + uwsgi

* Run:

```shell
./run.sh async-gevent-uwsgi io
```

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
Number of failure:    0
Request per second:   38.768571178214174 [#/sec] (mean)
Time per request:     2277.77641693751 [ms] (mean)
 50%   2166.294813156128
 60%   2343.5468673706055
 70%   2510.529041290283
 80%   2742.1278953552246
 90%   3061.3949298858643
100%   3509.709119796753
```

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
Request per second:   67.14033580860917 [#/sec] (mean)
Time per request:     1268.4854102134705 [ms] (mean)
 50%   1187.110185623169
 60%   1269.5260047912598
 70%   1327.55708694458
 80%   1482.7969074249268
 90%   1655.9088230133057
100%   1906.9247245788574
```



### Flask + gevent + gunicorn

* Run:

```shell
./run.sh async-gevent-gunicorn io
```

#### 1 process

```sh
gunicorn --worker-class gevent \
  --workers 1 \
  --bind 0.0.0.0:3000 \ 
  patched:app
```

```
Number of failure:    0
Request per second:   37.41417730412123 [#/sec] (mean)
Time per request:     2411.200877825419 [ms] (mean)
 50%   2573.1232166290283
 60%   2841.3071632385254
 70%   2911.8728637695312
 80%   2977.699041366577
 90%   3069.3562030792236
100%   3119.6868419647217
```

#### 4 processes

```sh
gunicorn --worker-class gevent \
  --workers 4 \
  --bind 0.0.0.0:3000 \ 
  patched:app
```

```
Number of failure:    0
Request per second:   63.94880075720626 [#/sec] (mean)
Time per request:     1352.445782025655 [ms] (mean)
 50%   1282.0079326629639
 60%   1330.4710388183594
 70%   1429.2209148406982
 80%   1546.360969543457
 90%   1708.1139087677002
100%   2742.5589561462402
```



### FastAPI + uvicorn

* Run:

```shell
./run.sh async-fastapi io
```

#### 1 process

```sh
uvicorn --host 0.0.0.0 --port 3000 --workers 1 'app:app'
```

```
Number of failure:    0
Request per second:   61.20740290304029 [#/sec] (mean)
Time per request:     1444.407479763031 [ms] (mean)
 50%   1404.0629863739014
 60%   1492.171049118042
 70%   1608.8378429412842
 80%   1750.4887580871582
 90%   1826.8890380859375
100%   1887.2241973876953
```

#### 4 processes

```sh
uvicorn --host 0.0.0.0 --port 3000 --workers 4 'app:app'
```

```
Number of failure:    0
Request per second:   60.65715835880818 [#/sec] (mean)
Time per request:     1266.7906538645427 [ms] (mean)
 50%   1222.5501537322998
 60%   1253.734827041626
 70%   1303.7891387939453
 80%   1362.6608848571777
 90%   1468.2257175445557
100%   2406.4788818359375
```



### FastAPI + uvicorn + gunicorn

* Run:

```shell
./run.sh async-fastapi-gunicorn io
```

#### 1 process

```sh
gunicorn --worker-class uvicorn.workers.UvicornWorker \
  --workers 1 \
  --bind "0.0.0.0:3000" \
  'app:app'
```

```
Number of failure:    0
Request per second:   58.71871169788235 [#/sec] (mean)
Time per request:     1507.2543168067932 [ms] (mean)
 50%   1477.311134338379
 60%   1632.7061653137207
 70%   1680.1762580871582
 80%   1848.5918045043945
 90%   1884.8762512207031
100%   2598.2658863067627
```

#### 4 processes

```sh
gunicorn --worker-class uvicorn.workers.UvicornWorker \
  --workers 4 \
  --bind "0.0.0.0:3000" \
  'app:app'
```

```
Number of failure:    0
Request per second:   60.201760316949674 [#/sec] (mean)
Time per request:     1331.1211562156677 [ms] (mean)
 50%   1279.8800468444824
 60%   1306.6790103912354
 70%   1365.2958869934082
 80%   1437.108039855957
 90%   1536.6239547729492
100%   2532.7329635620117
```



### async gRPC 

* Run

```shell
./run.sh async-grpc io
```

```sh
python app.py
```

```
Number of failure:    0
Request per second:   9.466468282971666 [#/sec] (mean)
Time per request:     10338.490180969238 [ms] (mean)
 50%   10239.897727966309
 60%   10282.15503692627
 70%   10315.02103805542
 80%   10587.954998016357
 90%   10928.998947143555
100%   11249.37891960144
```

