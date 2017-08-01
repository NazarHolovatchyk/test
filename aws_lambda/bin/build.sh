#!/usr/bin/env bash

color() {
  local COLOR_OFF='\033[0m'
  local RED='\033[1;31m'
  local GREEN='\033[1;32m'
  local YELLOW='\033[1;33m'
  local COLOR=$1
  local TEXT=$2
  case "${COLOR}" in
    red    |  r) CODE=${RED};;
    green  |  g) CODE=${GREEN};;
    yellow |  y) CODE=${YELLOW};;
  esac
  echo "${CODE}${TEXT}${COLOR_OFF}"
}

# exit on an error
set -e
# verbose mode
# set -x

STAGE=${1:-prod}

cd `dirname $0`/../
LAMBDA_BASE_DIR=$(pwd)
BUILD_DIR=${LAMBDA_BASE_DIR}/build
DIST_DIR=${LAMBDA_BASE_DIR}/dist

#VERSION=$(git tag --points-at HEAD || git rev-parse HEAD)
VERSION=$(git rev-parse HEAD)
color green "Building lambdas for ${STAGE} version: ${VERSION:0:10}"

# Cleanup and prepare
rm -rf ${BUILD_DIR}
rm -rf ${DIST_DIR}
mkdir ${BUILD_DIR}
mkdir ${DIST_DIR}

# copy code
cp -R alexa/* ${BUILD_DIR}
cd ${BUILD_DIR}

# create packages
for JOB_DIR in $(ls -d */)
do
    JOB=$(echo ${JOB_DIR} | tr -d '/')
    color green "Building package for ${JOB} job"
    JOB_PATH=${BUILD_DIR}/${JOB}
    pushd ${JOB_PATH}
    docker run --rm -v ${JOB_PATH}:/var/task -v /tmp/.pip-cache:/tmp/.pip-cache \
        lambci/lambda:build-python2.7 \
        pip install pip==8.1.1 && \
        pip install -r requirements.txt -t ${JOB_PATH} --cache-dir=/tmp/.pip-cache/

    cp ${LAMBDA_BASE_DIR}/context/${STAGE}.json ${JOB_PATH}/.context
    cp -R ${LAMBDA_BASE_DIR}/common ${JOB_PATH}
    find . -name "*.pyc" -delete
    find . -name ".DS_Store" -delete
    echo "[install]" > ${JOB_PATH}/setup.cfg
    echo "prefix=" >> ${JOB_PATH}/setup.cfg
    popd
    color green "Archiving package"
    zip -r -q ${DIST_DIR}/${JOB}.zip .
done

# cleanup
#rm -rf ${BUILD_DIR}

color green "Packages created in ${DIST_DIR}"
