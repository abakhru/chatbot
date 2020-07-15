#!/bin/bash

export PYTHONPATH=${WORKSPACE}
export PYTHONIOENCODING=utf-8
export WORKSPACE=${PWD}
export VIRTUAL_ENV=${VIRTUAL_ENV:-$WORKSPACE/env}

cd "${WORKSPACE}"
echo "Creating Vritualenv for the project"
if [ ! -d ${VIRTUAL_ENV} ]; then
  python3 -m venv ${VIRTUAL_ENV}
fi

echo "Installing python dependeny packages"
"${VIRTUAL_ENV}"/bin/pip install -U pip setuptools wheel
"${VIRTUAL_ENV}"/bin/pip install -e .
source "${VIRTUAL_ENV}"/bin/activate
