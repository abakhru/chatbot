FROM python:3.8-slim-buster
LABEL maintainer="amit <bakhru@me.com>"

ENV USER=botuser
# create a non-root default user
RUN useradd -m -d /home/${USER} -s /bin/bash ${USER} && \
    echo "${USER}:${USER}" | chpasswd && \
    adduser ${USER} sudo

RUN apt update && \
    apt full-upgrade -y && \
    apt autoremove -y && \
    apt install -y --no-install-recommends curl && \
    apt clean && apt autoremove -y && rm -rf /var/lib/apt/lists/* && \
    mkdir -p /app/chatbot && \
    chown -R ${USER}:${USER} /app && \
    python3 -m pip install -q --pre poetry && \
    python3 -m pip install -q -U pip setuptools

USER ${USER}
COPY pyproject.toml poetry.lock /app/
COPY chatbot/* /app/chatbot/

USER ${USER}
WORKDIR /app
RUN python3 -m poetry install -vv && \
    # download nltk files
    python3 -m poetry run python -c "import nltk; nltk.download('punkt', quiet=False)" && \
    python3 -m poetry run python -c "import nltk; nltk.download('wordnet', quiet=False)" && \
    python3 -m poetry run python -c "import nltk; nltk.download('averaged_perceptron_tagger', quiet=False)"

CMD ["/usr/local/bin/poetry", "run", "python", "chatbot/bot.py"]
