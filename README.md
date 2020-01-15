### Simple chatbot 

- normal HR related query conversation
- wikipedia search
- google search

### Install Poetry
```.bash
python3 -m pip install --pre poetry
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
- for mitre T-id search `mitre T1105`
- for mitre attack type search `mitre Management`, will list attack types with T<id>

### build docker images
```
cd ~/src/chatbot && docker build -t chatbot -f chatbot/Dockerfile .
```

#### run with docker container
```
docker run -it --rm chatbot bash
```

#### geoip db update
```
# install https://github.com/maxmind/geoipupdate
# download latest database using following command:
cd ~/src/chatbot && geoipupdate -f config/GeoIP.conf --database-directory ./data -v
```

### Reference:
- https://towardsdatascience.com/lets-build-an-intelligent-chatbot-7ea7f215ada6?gi=da4ec7aa5db6
- other NLTK data location: http://www.nltk.org/nltk_data/

### Code formatting using Black. Install the pre-commit hook:
```
brew install pre-commit
cd ~/src/chatbot; pre-commit install
# black --config ./pyproject.toml .  <= only needed if you need to format whole project files
```
- Now do the code changes as necessary and when you perform `git commit`, black would auto
  -format changed files and you can review and git add those files for commit
 
### TODO
- [x] mitre data search and co-relation
- [ ] more natural conversational
- [ ] search videos, news etc
- [ ] [`tqdm`](https://github.com/tqdm/tqdm) support for search wait-time
- [x] add [`fastapi`](https://github.com/tiangolo/fastapi) web framework for REST/Web access
- [ ] add [`click`](https://github.com/pallets/click) cli support
- [ ] integrate more sources/features
  - [x] google search
  - [ ] twitter feed
  - [x] maxmind geoip lookup
  - [x] whois lookup
- [ ] add more topic related source urls
- [ ] package the application using [`PyOxidizer`](https://github.com/indygreg/PyOxidizer)
- [x] add tests
- [x] add colored logger
- [x] Dockerize the application
- [x] add [netdata](https://github.com/netdata/netdata) monitoring support
- [x] add support for pre-commit and black code auto-formatters
