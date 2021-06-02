#!/bin/bash -x

set -xe
export WORKSPACE=${PWD}
export PYTHONPATH=${WORKSPACE}
export PYTHONIOENCODING=utf-8
export VIRTUAL_ENV=${VIRTUAL_ENV:$HOME/env}

cd "${WORKSPACE}"
if [ ! -d "${VIRTUAL_ENV}" ]; then
  python3 -m venv "${VIRTUAL_ENV}"
fi
source "${VIRTUAL_ENV}/bin/activate"

"${VIRTUAL_ENV}"/bin/pip install -U pip setuptools wheel
"${VIRTUAL_ENV}"/bin/pip install -e .

"${VIRTUAL_ENV}"/bin/python -c "import nltk; nltk.download('punkt', quiet=False)"
"${VIRTUAL_ENV}"/bin/python -c "import nltk; nltk.download('wordnet', quiet=False)"
"${VIRTUAL_ENV}"/bin/python -c "import nltk; nltk.download('averaged_perceptron_tagger', quiet=False)"