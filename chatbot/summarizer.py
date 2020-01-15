#!/usr/bin/env python

"""
reference: https://www.analyticsvidhya.com/blog/2018/11/introduction-text-summarization-textrank-python/
"""
from pathlib import Path

import networkx
import nltk
import numpy
import requests
from nltk.cluster.util import cosine_distance
from nltk.corpus import stopwords

from chatbot import LOGGER

nltk.download('stopwords', quiet=True)


class ExtractiveTextSummarizer:
    def __init__(self, file_name):
        self.file = Path(file_name)
        self.stop_words = stopwords.words('english')
        assert self.file.exists(), f'FileNotFoundError => {self.file}'

    def read_article(self):
        """2. Generate clean sentences"""
        article = self.file.read_text().split('. ')
        sentences = list()
        for sentence in article:
            # remove punctuations, numbers and special characters
            sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
            # sentences.pop()
        return sentences

    # Build similarity matrix
    def sentence_similarity(self, sent1, sent2):
        """This is where we will be using cosine similarity to find similarity between sentences."""

        # make alphabets lowercase
        sent1 = [w.lower() for w in sent1]
        sent2 = [w.lower() for w in sent2]

        all_words = list(set(sent1 + sent2))

        vector1 = [0] * len(all_words)
        vector2 = [0] * len(all_words)

        # remove stopwords
        # build the vector for the first sentence
        for w in sent1:
            if w in self.stop_words:
                continue
            vector1[all_words.index(w)] += 1

        # build the vector for the second sentence
        for w in sent2:
            if w in self.stop_words:
                continue
            vector2[all_words.index(w)] += 1
        return 1 - cosine_distance(vector1, vector2)

    def build_similarity_matrix(self, sentences):
        # Create an empty similarity matrix
        similarity_matrix = numpy.zeros((len(sentences), len(sentences)))

        for idx1 in range(len(sentences)):
            for idx2 in range(len(sentences)):
                if idx1 == idx2:  # ignore if both are same sentences
                    continue
                similarity_matrix[idx1][idx2] = self.sentence_similarity(
                    sentences[idx1], sentences[idx2]
                )
        return similarity_matrix

    def generate_summary(self, top_n=5):
        """Generate summary method"""
        summarize_text = list()
        # Step 1 - Read text and tokenize
        sentences = self.read_article()
        LOGGER.debug(f'sentences: {sentences}')
        # Step 2 - Generate Similarity matrix across sentences
        sentence_similarity_matrix = self.build_similarity_matrix(sentences)
        LOGGER.debug(f'sentence_similarity_matrix: {sentence_similarity_matrix}')
        # Step 3 - Rank sentences in similarity matrix
        sentence_similarity_graph = networkx.from_numpy_array(sentence_similarity_matrix)
        LOGGER.debug(f'sentence_similarity_graph: {sentence_similarity_graph}')
        scores = networkx.pagerank(sentence_similarity_graph)
        LOGGER.debug(f'scores: {scores}')
        # Step 4 - Sort the rank and pick top sentences
        ranked_sentence = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
        LOGGER.debug(f"Indexes of top ranked_sentence order are: {ranked_sentence}")

        for i in range(top_n):
            summarize_text.append(" ".join(ranked_sentence[i][1]))
            # Step 5 - Output the summarize text
        final_summarized_text = "\n".join([f'{i}.' for i in summarize_text])
        LOGGER.info(f'Summarize Text: \n{final_summarized_text}')


if __name__ == '__main__':
    # t = """In an attempt to build an AI-ready workforce, Microsoft announced Intelligent Cloud Hub which has been launched to empower the next generation of students with AI-ready skills. Envisioned as a three-year collaborative program, Intelligent Cloud Hub will support around 100 institutions with AI infrastructure, course content and curriculum, developer support, development tools and give students access to cloud and AI services. As part of the program, the Redmond giant which wants to expand its reach and is planning to build a strong developer ecosystem in India with the program will set up the core AI infrastructure and IoT Hub for the selected campuses. The company will provide AI development tools and Azure AI services such as Microsoft Cognitive Services, Bot Services and Azure Machine Learning. According to Manish Prakash, Country General Manager-PS, Health and Education, Microsoft India, said, "With AI being the defining technology of our time, it is transforming lives and industry and the jobs of tomorrow will require a different skillset. This will require more collaborations and training and working with AI. That’s why it has become more critical than ever for educational institutions to integrate new cloud and AI technologies. The program is an attempt to ramp up the institutional set-up and build capabilities among the educators to educate the workforce of tomorrow." The program aims to build up the cognitive skills and in-depth understanding of developing intelligent cloud connected solutions for applications across industry. Earlier in April this year, the company announced Microsoft Professional Program In AI as a learning track open to the public. The program was developed to provide job ready skills to programmers who wanted to hone their skills in AI and data science with a series of online courses which featured hands-on labs and expert instructors as well. This program also included developer-focused AI school that provided a bunch of assets to help build AI skills."""
    t = requests.get(
        url='https://timesofindia.indiatimes.com/india/congress-ncp-likely-to-insist'
        '-on-uddhav-thackeray-as-shiv-senas-pick-for-maharashtra-cm/articleshow'
        '/72078888.cms'
    ).content.decode()
    t1 = Path('/tmp/t')
    # if not t1.exists():
    t1.write_text(t)
    p = ExtractiveTextSummarizer(file_name='/tmp/t')
    p.generate_summary(top_n=2)
