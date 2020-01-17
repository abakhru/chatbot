FROM python:3.8-slim-buster
LABEL maintainer="amit <bakhru@me.com>"

# set environment variables
ENV USER=botuser PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 WORKDIR=/app

# set work directory
WORKDIR ${WORKDIR}

# create a non-root default user
RUN useradd -m -d /home/${USER} -s /bin/bash ${USER} && \
    echo "${USER}:${USER}" | chpasswd && \
    adduser ${USER} sudo

RUN apt update && \
    apt full-upgrade -y && \
    apt autoremove -y && \
    apt install -y --no-install-recommends curl gcc libc-dev libressl-dev libffi-dev \
    musl-dev python3-dev build-base build-deps && \
    apt clean && apt autoremove -y && rm -rf /var/lib/apt/lists/* && \
    mkdir -p ${WORKDIR}/chatbot && rm -rf /home/${USER}/.cache/pip \
    chown -R ${USER}:${USER} ${WORKDIR}

RUN python3 -m pip install -q -U pip setuptools && \
    python3 -m pip install -q --pre poetry

USER ${USER}
COPY pyproject.toml ${WORKDIR}/
COPY chatbot/* ${WORKDIR}/chatbot/

USER ${USER}
RUN python3 -m poetry install && \
    # download nltk files
    python3 -m poetry run python -c "import nltk; nltk.download('punkt', quiet=False)" && \
    python3 -m poetry run python -c "import nltk; nltk.download('wordnet', quiet=False)" && \
    python3 -m poetry run python -c "import nltk; nltk.download('averaged_perceptron_tagger', quiet=False)" && \
    echo 'source "$(poetry env info -p)/bin/activate"' >> /home/${USER}/.bashrc

CMD ["bash", "-c", "python", "-m uvicorn main:app --reload"]
