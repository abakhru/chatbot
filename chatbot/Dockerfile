FROM ubuntu:19.10
LABEL maintainer="amit <bakhru@me.com>"

# set environment variables
ENV USER=botuser PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 WORKDIR=/app DEBIAN_FRONTEND=noninteractive
ARG PG_VERSION=11

# set work directory
WORKDIR ${WORKDIR}

COPY . ${WORKDIR}/
RUN apt update && \
    apt full-upgrade -y && \
    apt autoremove -y && \
    apt install -y curl gcc libc-dev build-essential musl-dev sudo vim geoipupdate \
    libffi-dev postgresql-${PG_VERSION} postgresql-server-dev-${PG_VERSION} \
    python3 python3-venv python3-dev && \
    apt clean && apt autoremove -y && rm -rf /var/lib/apt/lists/* && \
    mkdir -p ${WORKDIR}/data && \
    chown -R ${USER}:${USER} ${WORKDIR}

# create a non-root default user
RUN useradd -m -d /home/${USER} -s /bin/bash ${USER} && \
    echo "${USER}:${USER}" | chpasswd && \
    adduser ${USER} sudo

USER ${USER}
RUN cd ${WORKDIR} && ./bin/quick_start.sh && \
    echo "alias l='ls -larth'" >> /home/${USER}/.bashrc && \
    # download nltk files
    ${WORKDIR}/env/bin/python -c "import nltk; nltk.download('punkt', quiet=False)" && \
    ${WORKDIR}/env/bin/python -c "import nltk; nltk.download('wordnet', quiet=False)" && \
    ${WORKDIR}/env/bin/python -c "import nltk; nltk.download('averaged_perceptron_tagger', quiet=False)"

CMD ["bash", "-c", "${WORKDIR}/env/bin/python", "-m uvicorn main:app --reload"]
