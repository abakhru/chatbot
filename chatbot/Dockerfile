FROM python:3.7-slim-buster
LABEL maintainer="amit <bakhru@me.com>"

RUN apt update && \
    apt full-upgrade -y && \
    apt autoremove -y && \
    apt install -y --no-install-recommends curl && \
    apt clean && apt autoremove -y && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /app/chatbot
WORKDIR /app

# install poetry
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python && \
    /root/.poetry/bin/poetry self:update --preview && \
    sed -i 's/python/python3/' /root/.poetry/bin/poetry

COPY pyproject.toml poetry.lock /app/
COPY chatbot/* /app/chatbot/
RUN /root/.poetry/bin/poetry install

# download nltk files
RUN /root/.poetry/bin/poetry run python -c "import nltk; nltk.download('punkt', quiet=False)" && \
    /root/.poetry/bin/poetry run python -c "import nltk; nltk.download('wordnet', quiet=False)" && \
    /root/.poetry/bin/poetry run python -c "import nltk; nltk.download('averaged_perceptron_tagger', quiet=False)"
CMD ["/root/.poetry/bin/poetry", "run", "python", "chatbot/bot.py"]
