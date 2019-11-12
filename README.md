### Simple chatbot 

- normal HR related query conversation
- wikipedia search
- google search

### Install Poetry
```.bash
# install poetry
curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python;
# for macos
sed -i '' 's/python/python3/' ~/.poetry/bin/poetry && . ~/.poetry/env
# for *unix platforms
sed -i 's/python/python3/' ~/.poetry/bin/poetry && . ~/.poetry/env
poetry self:update --preview && poetry --version
# makse sure the version is >=1.0.0b3 after update 
```

### install and run chatbot
```.env
git clone https://github.com/abakhru/chatbot.git && cd chatbot
poetry shell && poetry install && poetry show --tree
```

### Run the bot
```
./chatbot/bot.py
```
- for wikipedia search `wiki <search string>`
- for google search `google <search string>`

### Reference:
- https://towardsdatascience.com/lets-build-an-intelligent-chatbot-7ea7f215ada6?gi=da4ec7aa5db6


### TODO
- [ ] integrate more features: bing search, ?
- [x] add colored logger
- [ ] more natural conversational
- [ ] search videos, news etc
- [ ] tqdm support for search wait-time
