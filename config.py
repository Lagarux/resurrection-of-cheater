import os
import sys
import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv

# --- BASE_PATH ve bundle_dir Belirleme ---
if getattr(sys, 'frozen', False):
    BASE_PATH = os.path.dirname(sys.executable)
    bundle_dir = getattr(sys, '_MEIPASS', os.path.join(BASE_PATH, '_internal'))
else:
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    bundle_dir = BASE_PATH

# --- .env Dosyasını Arama Mantığı ---
possible_paths = [
    os.path.join(bundle_dir, '.env'),
    os.path.join(BASE_PATH, '.env'),
    os.path.join(BASE_PATH, '_internal', '.env'),
]

env_path = None
for p in possible_paths:
    if os.path.exists(p):
        env_path = p
        break

# .env bulunduysa yükle
if env_path:
    load_dotenv(dotenv_path=env_path)

# Anahtarı oku
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- KRİTİK KONTROL: Anahtar Yüklendi mi? ---
if not GEMINI_API_KEY:
    root = tk.Tk()
    root.withdraw()
    msg = (f"HATA: API Anahtarı yüklenemedi!\n\n"
           f"Aranan Dosya: .env\n"
           f"Bulunduğu Yol: {env_path if env_path else 'Bulunamadı'}\n\n"
           f"Lütfen .env dosyasının doğru konumda ve içinde "
           f"GEMINI_API_KEY tanımının olduğundan emin olun.")
    messagebox.showerror("API Key Hatası", msg)
    root.destroy()
    sys.exit(1)

# Tesseract ve Assets yolları aynı kalıyor...
TESSERACT_PATH = os.path.join(BASE_PATH, "Tesseract-OCR", "tesseract.exe")
TESSDATA_PREFIX = os.path.join(BASE_PATH, "Tesseract-OCR", "tessdata")
ICON_PATH = os.path.join(BASE_PATH, "assets", "RoC.ico")
# ... (LOCALIZATION ayarları aynı kalsın)

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