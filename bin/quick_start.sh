#!/bin/bash -x

export PYTHONPATH=${WORKSPACE}
export PYTHONIOENCODING=utf-8
export WORKSPACE=${PWD}
export VIRTUAL_ENV=${WORKSPACE}/env

cd "${WORKSPACE}"
if [ ! -d ${VIRTUAL_ENV} ]; then
  python3 -m venv ${VIRTUAL_ENV}
fi

"${VIRTUAL_ENV}"/bin/pip install -q -U pip setuptools wheel
"${VIRTUAL_ENV}"/bin/pip install -q -e .
source "${VIRTUAL_ENV}"/bin/activate
