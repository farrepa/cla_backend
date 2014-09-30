#!/bin/bash
set -e
CLA_DOCKER_REGISTRY=docker.cla.dsd.io

[[ $(curl -o /dev/null --silent --head --write-out '%{http_code}\n' http://$CLA_DOCKER_REGISTRY/v1/repositories/cla_frontend/images) == '200' ]] || { echo -e "\nTHE DOCKER REGISTRY IS DOWN!"; exit 1; }

sudo docker build --force-rm=true -t $CLA_DOCKER_REGISTRY/$APP_NAME .
sudo docker tag $CLA_DOCKER_REGISTRY/$APP_NAME $CLA_DOCKER_REGISTRY/$APP_NAME:$GIT_COMMIT
sudo docker push $CLA_DOCKER_REGISTRY/$APP_NAME
