FROM python:3.8-slim-buster
LABEL maintainer="amit <bakhru@me.com>"

# set environment variables
ENV USER=botuser PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 WORKDIR=/app
ENV VIRTUAL_ENV=${WORKDIR}/env HOME=/home/${USER} DEBIAN_FRONTEND=noninteractive
ARG UID=1000

# set work directory
WORKDIR ${WORKDIR}
COPY . ${WORKDIR}

# create a non-root default user
RUN useradd -m -d /home/${USER} -s /bin/bash ${USER} && \
    echo "${USER}:${USER}" | chpasswd && adduser ${USER} sudo && \
    chown -R "${USER}:${USER}" "${HOME}" && \
    echo "${USER} ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers && \
    chown -R ${USER}:${USER} ${WORKDIR}

RUN apt update && \
    apt full-upgrade -y && \
    apt install -y --no-install-recommends \
    build-essential \
    curl \
    gcc \
    libc-dev \
    libffi-dev \
    musl-dev \
    libpq-dev \
    python-pyaudio \
    python3-pyaudio \
    swig \
    git \
    libpulse-dev \
    libasound2-dev \
    python3-all-dev && \
    apt clean && apt autoremove -y && rm -rf /var/lib/apt/lists/*

USER ${USER}
RUN ./quick_start.sh

CMD ["bash", "-c", "${VIRTUAL_ENV}/bin/python", "-m uvicorn main:app --reload"]
