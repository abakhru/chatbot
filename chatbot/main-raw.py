import os
from glob import glob

import aiml

kernel = aiml.Kernel()

if os.path.isfile("bot_brain.brn"):
    kernel.bootstrap(brainFile="bot_brain.brn")
else:
    kernel.bootstrap(learnFiles=glob(f'{os.getenv("VIRTUAL_ENV")}/**/*.aiml',
                                     recursive=True),
                     commands="load aiml b")
    kernel.saveBrain("bot_brain.brn")

# kernel now ready for use
while True:
    message = input("Enter your message to the bot: ")
    if message == "quit":
        exit()
    elif message == "save":
        kernel.saveBrain("bot_brain.brn")
    else:
        bot_response = kernel.respond(message)
        print(bot_response)
