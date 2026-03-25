import os
import sys
from dotenv import load_dotenv

# .env dosyasındaki değişkenleri yükle
load_dotenv()

# API Key artık güvenli bir şekilde dışarıdan okunuyor
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- BASE_PATH: Uygulamanın çalıştığı ana dizini belirler ---
# Eğer uygulama .exe (frozen) halindeyse sys.executable kullanır, 
# .py halindeyse dosyanın kendi konumunu baz alır.
if getattr(sys, 'frozen', False):
    # .exe olarak çalışırken .exe'nin olduğu klasör
    BASE_PATH = os.path.dirname(sys.executable)
else:
    # .py olarak çalışırken dosyanın olduğu klasör
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# --- API Anahtarı ---
GEMINI_API_KEY = "AIzaSyCPyc8JoJ7D3t00CUKL3mdpNPKwfGz8QKA"

# --- Tesseract Yolları ---
TESSERACT_PATH = os.path.join(BASE_PATH, "Tesseract-OCR", "tesseract.exe")
TESSDATA_PREFIX = os.path.join(BASE_PATH, "Tesseract-OCR", "tessdata")

# --- Varlık (Assets) Yolları ---
ICON_PATH = os.path.join(BASE_PATH, "assets", "RoC.ico")
FONT_PATH = os.path.join(BASE_PATH, "assets", "fonts", "BodoniModa.ttf")

# --- Dil ve Yerelleştirme Ayarları ---
LOCALIZATION = {
    "Türkçe": {
        "title": "RESURRECTION OF CHEATER",
        "source": "KAYNAK METİN",
        "result": "AI ANALİZİ VE ÇEVİRİ",
        "btn_snip": "📸 ALAN SEÇ",
        "btn_trans": "🌍 HIZLI ÇEVİR",
        "btn_ai": "🧠 AI ANALİZ",
        "btn_speak": "🔊 OKU",
        "ai_prompt": "Metni analiz et ve temiz bir markdown (başlık, kalın metin, liste) ile sun:\n\n"
    },
    "English": {
        "title": "RESURRECTION OF CHEATER",
        "source": "SOURCE TEXT",
        "result": "AI ANALYSIS AND TRANSLATION",
        "btn_snip": "📸 SNIP & READ",
        "btn_trans": "🌍 QUICK TRANS",
        "btn_ai": "🧠 AI ANALYZE",
        "btn_speak": "🔊 SPEAK",
        "ai_prompt": "Analyze the text and present it in clean markdown (headings, bold, lists):\n\n"
    }
}