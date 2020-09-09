FROM python:3.8-slim-buster
LABEL maintainer="amit <bakhru@me.com>"

# set environment variables
ENV USER=botuser PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 WORKDIR=/app
ENV VIRTUAL_ENV=${WORKDIR}/env

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
    chown -R ${USER}:${USER} ${WORKDIR}

USER ${USER}
COPY . ${WORKDIR}/chatbot/

USER ${USER}
RUN python3 -m venv ${VIRTUAL_ENV} && \
    # download nltk files
    ${VIRTUAL_ENV}/bin/python -c "import nltk; nltk.download('punkt', quiet=False)" && \
    ${VIRTUAL_ENV}/bin/python -c "import nltk; nltk.download('wordnet', quiet=False)" && \
    ${VIRTUAL_ENV}/bin/python -c "import nltk; nltk.download('averaged_perceptron_tagger', quiet=False)" && \

CMD ["bash", "-c", "${VIRTUAL_ENV}/bin/python", "-m uvicorn main:app --reload"]
