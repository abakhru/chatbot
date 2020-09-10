#!/bin/bash

export VIRTUAL_ENV=${VIRTUAL_ENV:-$WORKDIR/env}
"$VIRTUAL_ENV"/bin/python chatbot/bot.py
