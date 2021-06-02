#!/usr/bin/env python
import os
import subprocess
import urllib
import uuid
import wave
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import pathname2url

import newspaper
import pyaudio
import requests
import speech_recognition as sr
import urllib3
from bs4 import BeautifulSoup
from gtts import gTTS

from src import DATA_DIR, LOGGER

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
GOOGLE_CLOUD_SPEECH_CREDENTIALS = Path(os.getenv("GOOGLE_CLOUD_SPEECH_CREDENTIALS")).read_text()


class AudioManager:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.sr = sr.Recognizer()
        # TODO: cleanup DATA_DIR / 'temp_file_*.mp3' files

    def play_wav(self, audio_file):
        """ Play a WAVE file"""
        LOGGER.info(f'Playing audio file "{audio_file}"')
        if audio_file.endswith(".mp3"):
            return self.play_mp3(audio_file)
        wf = wave.open(audio_file, "rb")
        self.stream = self.p.open(
            format=self.p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True,
        )
        data = wf.readframes(CHUNK)
        while data != b"":
            self.stream.write(data)
            data = wf.readframes(CHUNK)
        wf.close()
        self.close()

    def record2(self, output_file="output.wav"):
        """real-time recording of voice and saving to wav format"""
        self.stream = self.p.open(
            format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
        )
        LOGGER.info("* recording")
        frames = []
        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = self.stream.read(CHUNK)
            frames.append(data)
        LOGGER.info("* done recording")
        wf = wave.open(output_file, "wb")
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))
        wf.close()
        self.close()

    def record(self, output_file="output.wav"):
        """real-time recording of voice from mac microphone and saving to wav format"""
        with sr.Microphone() as source:
            LOGGER.info("Say something!")
            audio = self.sr.listen(source, phrase_time_limit=RECORD_SECONDS)
        LOGGER.debug("Writing audio to a WAV file")
        Path(output_file).write_bytes(audio.get_wav_data())
        LOGGER.info("Done recording !")

    def speech_to_text_sphinx(self, audio_file):
        with sr.AudioFile(audio_file) as source:
            audio = self.sr.record(source)  # read the entire audio file
        try:
            LOGGER.info("Sphinx thinks you said " + self.sr.recognize_sphinx(audio))
        except sr.UnknownValueError:
            LOGGER.error("Sphinx could not understand audio")
        except sr.RequestError as e:
            LOGGER.error(f"Sphinx error; {e}")

        # write audio to a RAW file
        # with open("microphone-results.raw", "wb") as f:
        #     f.write(audio.get_raw_data())

        # # write audio to an AIFF file
        # with open("microphone-results.aiff", "wb") as f:
        #     f.write(audio.get_aiff_data())
        #
        # # write audio to a FLAC file
        # with open("microphone-results.flac", "wb") as f:
        #     f.write(audio.get_flac_data())

    def speech_to_text_google(self, audio_file):
        """recognize speech using Google Cloud Speech"""
        try:
            with sr.AudioFile(audio_file) as source:
                audio = self.sr.record(source)
            out = self.sr.recognize_google_cloud(
                audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS
            )
            LOGGER.info(f"[Speech2Text] {out}")
        except sr.UnknownValueError:
            LOGGER.error("Google Cloud Speech could not understand audio")
        except sr.RequestError as e:
            LOGGER.error(f"Could not request results from Google Cloud Speech service; {e}")

    @staticmethod
    def text_to_speech_google(text):
        temp_file = DATA_DIR.joinpath(f"temp_file_{uuid.uuid4()}.mp3")
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(temp_file.name)
        return temp_file.name

    @staticmethod
    def text_to_speech_mozilla(text):
        temp_file = DATA_DIR.joinpath(f"temp_file_{uuid.uuid4()}.mp3")
        for part_text in text.split('.'):
            speech = requests.get('http://tts:5002/api/tts', params=f'text={part_text}')
            assert speech.status_code == 200
            assert speech.headers.get('Content-Type') == 'audio/wav'
            temp_file.write_bytes(speech.content)
        return temp_file.name

    @staticmethod
    def play_mp3(audio_file):
        return subprocess.check_output(f"vlc --play-and-exit {audio_file}", shell=True)

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()


class ArticleToSpeech:
    def __init__(self, url):
        self.url = url
        self.article = None

    def get_article(self):
        LOGGER.info(f'Retrieving the article from "{self.url}"')
        self.article = newspaper.Article(self.url)
        self.article.download()
        self.article.parse()
        return self.article.text

    def summarize(self):
        LOGGER.info(f'Summarizing the article ...')
        self.article.nlp()
        summary = self.article.summary
        LOGGER.info({summary})
        return summary


if __name__ == "__main__":
    p = AudioManager()
    news_article = 'https://openthemagazine.com/features/modi-at-70-a-style-statement/'
    c = ArticleToSpeech(news_article)
    article_body = c.get_article()
    ad_file = p.text_to_speech_mozilla(article_body)
    p.play_wav(audio_file=ad_file)
    # p.speech_to_text_google(audio_file=ad_file)
