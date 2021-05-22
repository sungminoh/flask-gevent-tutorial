#! /bin/sh
CYON='\033[0;36m'
NC='\033[0m'
NUM_REQUESTS=300
CONCURRENCY=100

build() {
  docker-compose -f deployments/${1}.yml build
  docker-compose -f deployments/${1}.yml up -d
}

wait_docker() {
  if [[ "$1" == *"grpc"* ]]; then
    while ! grpc_cli call localhost:3000 MyApp.index '' &> /dev/null
    do
      sleep 1;
    done
    sleep 1;
  else
    while ! curl -s 'http://127.0.0.1:3000' &> /dev/null
    do
      sleep 1;
    done
    sleep 1;
  fi
}

benchmark() {
  # Test single-threaded deployment
  echo "${CYON}############ ${1} ($2) benchmark ############${NC}"
  if [[ "$1" == *"grpc"* ]]; then
    python benchmark.py -n $NUM_REQUESTS -c $CONCURRENCY grpc $2
  else
    python benchmark.py -n $NUM_REQUESTS -c $CONCURRENCY http $2
    #if [[ "$2" == "io" ]]; then
      #url=http://127.0.0.1:3000/io_bound?delay=1
      #ab -r -l -n $NUM_REQUESTS -c $CONCURRENCY $url
      #curl -s $url
      #curl -s $url
      #curl -s $url
    #elif [[ "$2" == "cpu" ]]; then
      #url=http://127.0.0.1:3000/cpu_bound?num=1000
      #ab -r -l -n $NUM_REQUESTS -c $CONCURRENCY $url
      #curl -s $url
      #curl -s $url
      #curl -s $url
    #fi
  fi
}

down() {
  docker-compose -f deployments/${1}.yml down
}


if [ "$#" -eq 2 ]; then
  set -x
  build $1 > /dev/null
  wait_docker $1 > /dev/null
  benchmark $1 $2
  down $1
else
  echo "Usage: $0 [command] {io, cpu}, where command is one of the following:"
  ls "$(dirname $0)/deployments" | cut -d"." -f1
fi
