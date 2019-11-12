#!/usr/bin/env python
from builtins import Exception, dict, input, open, ord
from collections import defaultdict

import nltk
import random
import re
import string
import unicodedata
import warnings
import wikipedia as wk
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from serpapi.google_search_results import GoogleSearchResults
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

warnings.filterwarnings("ignore")
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)


class ChatBot:

    def __init__(self):
        self.data = open('/Users/amit/src/scratch/chatbot/data/HR.txt', 'r', errors='ignore')
        raw = self.data.read()
        raw = raw.lower()
        self.sent_tokens = nltk.sent_tokenize(raw)
        self.welcome_input = ("hello", "hi", "greetings", "sup", "what's up", "hey",)
        self.welcome_response = ["hi", "hey", "*nods*", "hi there", "hello",
                                 "I am glad! You are talking to me"]

    def start(self):
        flag = True
        print("My name is Chatterbot and I'm a chatbot. If you want to exit, type Bye!")
        while flag:
            user_response = input()
            user_response = user_response.lower()
            if user_response not in ['bye', 'shutdown', 'exit', 'quit']:
                if user_response == 'thanks' or user_response == 'thank you':
                    flag = False
                    print("Chatterbot : You are welcome..")
                else:
                    if self.welcome(user_response) is not None:
                        print(f'Chatterbot : {self.welcome(user_response)}')
                    else:
                        print("Chatterbot : ", end="")
                        print(self.generateResponse(user_response))
                        self.sent_tokens.remove(user_response)
            else:
                flag = False
                print("Chatterbot : Bye!!! ")

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
        tag_map = defaultdict(lambda: wn.NOUN)
        tag_map['J'] = wn.ADJ
        tag_map['V'] = wn.VERB
        tag_map['R'] = wn.ADV
        lmtzr = WordNetLemmatizer()
        lemma_list = []
        rmv = [i for i in rmv if i]
        for token, tag in nltk.pos_tag(rmv):
            lemma = lmtzr.lemmatize(token, tag_map[tag[0]])
            lemma_list.append(lemma)
        return lemma_list

    def welcome(self, user_response):
        for word in user_response.split():
            if word.lower() in self.welcome_input:
                return random.choice(self.welcome_response)

    def generateResponse(self, user_response):
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
        if (req_tfidf == 0) or "tell me about" in user_response:
            print("Checking Wikipedia")
            if user_response:
                robo_response = self.wikipedia_data(user_response)
                return robo_response
        if (req_tfidf == 0) or "google" in user_response:
            print("Checking Google")
            if user_response:
                robo_response = self.google_data(user_response)
                return robo_response
        else:
            robo_response = robo_response + self.sent_tokens[idx]
            return robo_response

    # wikipedia search
    def wikipedia_data(self, _input):
        reg_ex = re.search('tell me about (.*)', _input)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                wiki = wk.summary(topic, sentences=3)
                return wiki
        except Exception as _:
            print("No content has been found")

    # google search
    @staticmethod
    def google_data(_input):
        reg_ex = re.search('google (.*)', _input)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                response = GoogleSearchResults({"q": topic, "location": "Austin,Texas"})
                return response.get_dict()
        except Exception as _:
            print("No content has been found")


if __name__ == '__main__':
    p = ChatBot()
    p.start()
