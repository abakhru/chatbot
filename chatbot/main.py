"""https://github.com/sohelamin/chatbot"""

import os
from glob import glob
from pathlib import Path

import aiml
from fastapi import FastAPI

from chatbot.bot import ChatBot

app = FastAPI(__name__)
kernel = aiml.Kernel()
chat_bot = ChatBot()

if os.path.isfile("bot_brain.brn"):
    kernel.bootstrap(brainFile="bot_brain.brn")
else:
    kernel.bootstrap(
        learnFiles=glob(f'{os.getenv("VIRTUAL_ENV")}/**/*.aiml', recursive=True),
        commands="load aiml b",
    )
    kernel.saveBrain("bot_brain.brn")


@app.get("/")
def hello():
    chat_page = Path(__file__).parent.resolve().joinpath('templates', 'chat.html')
    return response.html(chat_page.read_text())


@app.route("/ask", methods=['POST'])
def ask(request):
    message = request.form['messageText'][0].strip()

    # kernel now ready for use
    while True:
        if message == "quit":
            exit()
        elif message == "save":
            kernel.saveBrain("bot_brain.brn")
        else:
            bot_response = kernel.respond(message)
            return response.json({'status': 'OK', 'answer': bot_response})


@app.route("/chat", methods=['POST'])
def chat(request):
    message = request.form['messageText'][0].strip()
    # kernel now ready for use
    while True:
        if message.lower() == "bye":
            exit()
        else:
            bot_response = chat_bot.respond(message)
            return response.json({'status': 'OK', 'answer': bot_response})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
