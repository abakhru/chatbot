#!/bin/bash

set -xe
export VIRTUAL_ENV=${VIRTUAL_ENV:-$HOME/env}
"$VIRTUAL_ENV"/bin/python src/bot.py
