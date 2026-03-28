from google import genai
from deep_translator import GoogleTranslator
from gtts import gTTS
import pygame, io, threading
from config import GEMINI_API_KEY

class AIManager:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        pygame.mixer.init()

    def analyze(self, prompt, text, callback, error_callback=None):
        def run():
            try:
                res = self.client.models.generate_content(model="gemini-3-flash-preview", contents=prompt + text)
                callback(res.text)
            except Exception as e:
                if error_callback:
                    error_callback(str(e))
        threading.Thread(target=run, daemon=True).start()

    def translate(self, text, target, callback, error_callback=None):
        def run():
            try:
                translated = GoogleTranslator(source='auto', target=target).translate(text)
                callback(translated)
            except Exception as e:
                if error_callback:
                    error_callback(str(e))
        threading.Thread(target=run, daemon=True).start()

    def speak(self, text, lang):
        def run():
            tts = gTTS(text=text, lang=lang)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            pygame.mixer.music.load(fp)
            pygame.mixer.music.play()
        threading.Thread(target=run, daemon=True).start()