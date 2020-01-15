#!/usr/bin/env python
import subprocess
from pathlib import Path
from subprocess import PIPE

import docker

home = Path(__file__).parent.parent.resolve()
client = docker.from_env()


def build_using_cli():
    cmd = f'(cd {home} && docker build -t chatbot -f chatbot/Dockerfile .)'
    print(cmd)
    p = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    while p.poll() is None:
        print(p.stdout.readlines().decode().rstrip(), flush=True)


if __name__ == '__main__':
    build_using_cli()
