#!/bin/bash -x

curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python;

if [ "$(uname -s)" = "Darwin" ]; then
  sed -i '' 's/python/python3/' ~/.poetry/bin/poetry && source "${HOME}/.poetry/env"
else
  # for *unix platforms
  sed -i 's/python/python3/' ~/.poetry/bin/poetry && source "${HOME}/.poetry/env"
fi

poetry self:update --preview && poetry --version