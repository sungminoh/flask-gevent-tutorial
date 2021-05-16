#! /bin/sh
CYON='\033[0;36m'
NC='\033[0m'

build() {
  docker-compose -f deployments/${1}.yml build
  docker-compose -f deployments/${1}.yml up -d
}

wait_docker() {
  while ! curl -s 'http://127.0.0.1:3000' > /dev/null
  do
    sleep 1;
  done
  sleep 1;
}

benchmark() {
  # Test single-threaded deployment
  echo "${CYON}############ ${1} deploayment ############${NC}"
  ab -r -l -n 600 -c 200 http://127.0.0.1:3000/?delay=1
  curl http://127.0.0.1:3000/?delay=1
  curl http://127.0.0.1:3000/?delay=1
  curl http://127.0.0.1:3000/?delay=1
}

down() {
  docker-compose -f deployments/${1}.yml down
}


if [ -n "$1" ]; then
  #set -x
  build $1 > /dev/null
  wait_docker $1 > /dev/null
  benchmark $1
  down $1
else
  echo "Usage: $0 [command], where command is one of the following:"
  ls "$(dirname $0)/deployments" | cut -d"." -f1
fi
