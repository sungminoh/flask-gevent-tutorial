# CPU bound

Api call runs `long_running(1000)`

```python
def long_running(n):
    m = np.random.random((100, 100))
    for _ in range(n):
        m *= np.random.random((100, 100)) + np.random.random((100, 100))
    return m
```

* Sync
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
./run.sh sync-devserver cpu
```

```shell
flask run --no-reload --without-threads --host 0.0.0.0 --port 3000
```

```
Number of failure:    0
Request per second:   7.467929534847055 [#/sec] (mean)
Time per request:     11154.896311759949 [ms] (mean)
 50%   13286.597967147827
 60%   13322.173833847046
 70%   13359.673023223877
 80%   13373.536109924316
 90%   13387.46190071106
100%   13425.304174423218
```

### Flask dev server with thread

* Run:

```shell
./run.sh sync-devserver-threaded cpu
```

```shell
flask run --no-reload --with-threads --host 0.0.0.0 --port 3000
```

```
Number of failure:    20
Request per second:   5.540495847307016 [#/sec] (mean)
Time per request:     16841.292837687903 [ms] (mean)
 50%   16996.027946472168
 60%   17699.36203956604
 70%   18516.866207122803
 80%   19429.68702316284
 90%   20597.601890563965
100%   23434.957265853882
```



### Flask + uwsgi

* Run:

```shell
./run.sh sync-uwsgi cpu
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
Request per second:   5.64788338737252 [#/sec] (mean)
Time per request:     15904.755013783773 [ms] (mean)
 50%   16695.81389427185
 60%   17459.49912071228
 70%   18125.29683113098
 80%   18707.233905792236
 90%   19703.637838363647
100%   22081.959009170532
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
Request per second:   5.572474005509042 [#/sec] (mean)
Time per request:     17251.304564476013 [ms] (mean)
 50%   17350.324869155884
 60%   18106.105089187622
 70%   18637.763738632202
 80%   19425.0910282135
 90%   20567.6429271698
100%   25108.788013458252
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
Request per second:   12.627538098466122 [#/sec] (mean)
Time per request:     7215.216914812724 [ms] (mean)
 50%   7263.333797454834
 60%   7804.434776306152
 70%   8483.943939208984
 80%   8972.388744354248
 90%   9328.765869140625
100%   10304.612159729004
```



### Flask + gunicorn

* Run:

```shell
./run.sh sync-gunicorn cpu
```

#### 1 process * 50 threads

```sh
gunicorn --workers 1 \
  --threads 50 \
  --bind 0.0.0.0:3000 \ 
  app:app
```

```
Number of failure:    14
Request per second:   5.542480016971969 [#/sec] (mean)
Time per request:     16063.41944624494 [ms] (mean)
 50%   17250.560998916626
 60%   17933.418035507202
 70%   18473.339319229126
 80%   19015.89298248291
 90%   19643.362760543823
100%   21852.71668434143
```

#### 1 process * 200 threads

```sh
gunicorn --workers 1 \
  --threads 200 \
  --bind 0.0.0.0:3000 \ 
  app:app
```

```
Number of failure:    2
Request per second:   5.578164715583498 [#/sec] (mean)
Time per request:     16106.153324146399 [ms] (mean)
 50%   17064.152717590332
 60%   17630.89084625244
 70%   18235.865116119385
 80%   18945.063829421997
 90%   19616.867065429688
100%   22542.083024978638
```

#### 4 processes * 50 threads

```sh
gunicorn --workers 4 \
  --threads 50 \
  --bind 0.0.0.0:3000 \ 
  app:app
```

```
Number of failure:    218
Request per second:   12.333039505910937 [#/sec] (mean)
Time per request:     5228.97303395155 [ms] (mean)
 50%   5333.8282108306885
 60%   5459.274053573608
 70%   5593.492031097412
 80%   5744.619131088257
 90%   5839.107990264893
100%   6021.569013595581
```



### gRPC 

* Run

```shell
./run.sh sync-grpc cpu
```

```sh
python app.py
```

```
Number of failure:    0
Request per second:   5.3186075531898815 [#/sec] (mean)
Time per request:     16018.229968547821 [ms] (mean)
 50%   18349.691152572632
 60%   18598.143100738525
 70%   18877.09093093872
 80%   19184.178829193115
 90%   19437.0539188385
100%   20542.484998703003
```





## Async

### Flask + gevent + uwsgi

* Run:

```shell
./run.sh async-gevent-uwsgi cpu
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
Request per second:   7.120115473542257 [#/sec] (mean)
Time per request:     11678.747042020163 [ms] (mean)
 50%   13808.922052383423
 60%   13890.512943267822
 70%   13980.952739715576
 80%   14129.01782989502
 90%   14208.554983139038
100%   14231.864929199219
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
Number of failure:    0
Request per second:   25.36693048821754 [#/sec] (mean)
Time per request:     3285.3859011332192 [ms] (mean)
 50%   3828.8722038269043
 60%   3877.9242038726807
 70%   3899.45912361145
 80%   3925.3649711608887
 90%   3957.124948501587
100%   4015.576124191284
```



### Flask + gevent + gunicorn

* Run:

```shell
./run.sh async-gevent-gunicorn cpu
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
Request per second:   7.129410354885129 [#/sec] (mean)
Time per request:     11669.809772968292 [ms] (mean)
 50%   13939.554929733276
 60%   14046.540975570679
 70%   14080.08599281311
 80%   14124.93085861206
 90%   14180.46498298645
100%   14214.695930480957
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
Request per second:   24.62895851425214 [#/sec] (mean)
Time per request:     3288.2320030530295 [ms] (mean)
 50%   3701.874256134033
 60%   3774.4691371917725
 70%   3953.185796737671
 80%   4207.694292068481
 90%   4391.623258590698
100%   4518.203258514404
```



### FastAPI + uvicorn

* Run:

```shell
./run.sh async-fastapi cpu
```

#### 1 process

```sh
uvicorn --host 0.0.0.0 --port 3000 --workers 1 'app:app'
```

```
Number of failure:    0
Request per second:   7.449747334395097 [#/sec] (mean)
Time per request:     13047.50405550003 [ms] (mean)
 50%   13386.197090148926
 60%   13406.09097480774
 70%   13423.70891571045
 80%   13438.914060592651
 90%   13492.16604232788
100%   13621.616840362549
```

#### 4 processes

```sh
uvicorn --host 0.0.0.0 --port 3000 --workers 4 'app:app'
```

```
Number of failure:    0
Request per second:   23.13420155375113 [#/sec] (mean)
Time per request:     3687.835521697998 [ms] (mean)
 50%   3237.870931625366
 60%   4409.748077392578
 70%   4507.19690322876
 80%   6092.8850173950195
 90%   6773.514032363892
100%   6896.636247634888
```



### FastAPI + uvicorn + gunicorn

* Run:

```shell
./run.sh async-fastapi-gunicorn cpu
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
Request per second:   7.135969034566336 [#/sec] (mean)
Time per request:     13692.229187488556 [ms] (mean)
 50%   13788.601875305176
 60%   13840.652227401733
 70%   14365.00597000122
 80%   14435.467004776001
 90%   14488.574028015137
100%   14537.456035614014
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
Request per second:   14.928957691633608 [#/sec] (mean)
Time per request:     5531.24623298645 [ms] (mean)
 50%   6333.323001861572
 60%   7766.646146774292
 70%   9253.05986404419
 80%   9363.178014755249
 90%   10515.977144241333
100%   10571.257829666138
```



### async gRPC 

* Run

```shell
./run.sh async-grpc cpu
```

```sh
python app.py
```

```
Number of failure:    0
Request per second:   7.453717219297743 [#/sec] (mean)
Time per request:     11201.641116937002 [ms] (mean)
 50%   13176.876068115234
 60%   13361.418724060059
 70%   13610.116958618164
 80%   13700.130939483643
 90%   13715.215921401978
100%   13764.955043792725
```

