#!/usr/bin/env python

import random
import re
import string
import unicodedata
import warnings
from collections import defaultdict
from pathlib import Path
from urllib.request import urlopen

import nltk
import requests
import wikipedia
from bs4 import BeautifulSoup
from googlesearch import search
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from nltk.chat.util import Chat


from chatbot import LOGGER, reflections, pairs

warnings.filterwarnings("ignore")
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

WELCOME_DICT = {"input": ["hello",
                          "hi",
                          "greetings",
                          "sup",
                          "what's up",
                          "hey"],
                "response": ["hi",
                             "hey",
                             "*nods*",
                             "hi there",
                             "hello",
                             "I am glad! You are talking to me"]}


class ChatBot:

    def __init__(self):
        self.sent_tokens = nltk.sent_tokenize(self.hr_data().lower())
        self.welcome_input = WELCOME_DICT['input']
        self.welcome_response = WELCOME_DICT['response']
        self.iesha_chatbot = Chat(pairs, reflections)

    def iesha_chat(self):
        print("Iesha the TeenBoT\n---------")
        print("Talk to the program by typing in plain English, using normal upper-")
        print('and lower-case letters and punctuation.  Enter "quit" when done.')
        print('=' * 72)
        print("hi!! i'm iesha! who r u??!")
        self.iesha_chatbot.converse()

    def hr_data(self):
        self.hr_data_path = Path('/tmp', '.HR.txt')
        if not self.hr_data_path.exists():
            r = requests.get(url='http://www.whatishumanresource.com/human-resource-management',
                             allow_redirects=True)
            self.hr_data_path.write_text(r.content.decode())
        self.hr_data_path.read_text()

    def mitre_data(self):
        self.mitre_data_path = Path('/tmp', '.mitre.txt')
        urls = ['https://www.exabeam.com/information-security/what-is-mitre-attck-an-explainer/',
                '']
        if not self.mitre_data_path.exists():
            r = requests.get(url='http://www.whatishumanresource.com/human-resource-management',
                             allow_redirects=True)
            self.hr_data_path.write_text(r.content.decode())
        self.hr_data_path.read_text()

    def start(self):
        flag = True
        LOGGER.info("My name is Chatterbot and I'm a chatbot. If you want to exit, type Bye!")
        while flag:
            user_response = input()
            user_response = user_response.lower()
            if user_response not in ['bye', 'shutdown', 'exit', 'quit']:
                if user_response == 'thanks' or user_response == 'thank you':
                    flag = False
                    LOGGER.info("Chatterbot : You are welcome..")
                else:
                    if self.welcome(user_response) is not None:
                        LOGGER.info(f'Chatterbot : {self.welcome(user_response)}')
                    else:
                        LOGGER.warning(f'{self.generate_response(user_response)}')
                        self.sent_tokens.remove(user_response)
            else:
                flag = False
                LOGGER.info("Chatterbot : Bye!!! ")

    def normalize(self, text):
        remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
        # word tokenization
        word_token = nltk.word_tokenize(text.lower().translate(remove_punct_dict))

        # remove ascii
        new_words = []
        for word in word_token:
            new_word = unicodedata.normalize('NFKD',
                                             word).encode('ascii',
                                                          'ignore').decode('utf-8', 'ignore')
            new_words.append(new_word)

        # Remove tags
        rmv = []
        for w in new_words:
            text = re.sub("&lt;/?.*?&gt;", "&lt;&gt;", w)
            rmv.append(text)

        # pos tagging and lemmatization
        tag_map = defaultdict(lambda: wordnet.NOUN)
        tag_map['J'] = wordnet.ADJ
        tag_map['V'] = wordnet.VERB
        tag_map['R'] = wordnet.ADV
        lmtzr = WordNetLemmatizer()
        lemma_list = list()
        rmv = [i for i in rmv if i]
        for token, tag in nltk.pos_tag(rmv):
            lemma = lmtzr.lemmatize(token, tag_map[tag[0]])
            lemma_list.append(lemma)
        return lemma_list

    def welcome(self, user_response):
        for word in user_response.split():
            if word.lower() in self.welcome_input:
                return random.choice(self.welcome_response)

    def generate_response(self, user_response):
        robo_response = ''
        self.sent_tokens.append(user_response)
        TfidfVec = TfidfVectorizer(tokenizer=self.normalize, stop_words='english')
        tfidf = TfidfVec.fit_transform(self.sent_tokens)
        # vals = cosine_similarity(tfidf[-1], tfidf)
        vals = linear_kernel(tfidf[-1], tfidf)
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        if (req_tfidf == 0) or "wiki" in user_response:
            LOGGER.info("Chatterbot : Checking Wikipedia")
            if user_response:
                robo_response = self.wikipedia_data(user_response)
                return robo_response
        if (req_tfidf == 0) or "google" in user_response:
            LOGGER.info("Chatterbot : Checking Google")
            if user_response:
                robo_response = self.google_data(user_response)
                return robo_response
        else:
            robo_response = robo_response + self.sent_tokens[idx]
            return robo_response

    # wikipedia search
    def wikipedia_data(self, _input):
        reg_ex = re.search('wiki (.*)', _input)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                wiki = wikipedia.summary(topic, sentences=3)
                return wiki
        except Exception as _:
            LOGGER.warning(f"No content for {_input} has been found")

    @staticmethod
    def google_data(_input):
        """google search"""
        reg_ex = re.search('google (.*)', _input)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                response = search(query=topic, num=10, stop=10)
                return '\n'.join(list(response))
        except Exception as _:
            LOGGER.warning(f"No URLs related to {_input} has been found")

    @staticmethod
    def twitter_data(_input):
        """twitter search"""
        reg_ex = re.search('twitter (.*)', _input)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                html = urlopen(f'https://twitter.com/search?q=#{topic}&src=typd')
                soup = BeautifulSoup(html.read(), 'html.parser')

        except Exception as _:
            LOGGER.warning(f"No URLs related to {_input} has been found")


if __name__ == '__main__':
    p = ChatBot()
    p.iesha_chat()
