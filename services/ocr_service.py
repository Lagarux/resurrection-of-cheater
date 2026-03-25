import pytesseract
from PIL import Image, ImageOps, ImageEnhance
from config import TESSERACT_PATH, TESSDATA_PREFIX
import os

# Tesseract yollarını global olarak mühürle
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
os.environ['TESSDATA_PREFIX'] = TESSDATA_PREFIX

class OCRManager:
    def __init__(self):
        # app.py'ın 'AttributeError' almaması için bu yolu sınıfa tanıtıyoruz
        self.tesseract_cmd = TESSERACT_PATH

    def process(self, img):
        img = img.convert('L')
        img = ImageEnhance.Contrast(img).enhance(3.0)
        img = ImageOps.expand(img, border=10, fill='white')
        img = img.resize((img.width*3, img.height*3), Image.Resampling.LANCZOS)
        
        custom_config = (
            r'--oem 3 --psm 6 -l tur+eng '
            r'-c preserve_interword_spaces=1 '
            r'-c "tessedit_char_whitelist=abcçdefgğhıijklmnoöprsştuüvyzABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ0123456789.,!?()+-=:; "'
            r'-c load_system_dawg=0 -c load_freq_dawg=0'
        )
        return pytesseract.image_to_string(img, config=custom_config).strip()