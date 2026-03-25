import os
import sys
import ctypes
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import pyautogui

# --- 1. Windows App ID Tanımlama ---
# Görev çubuğunda doğru ikonu ve ismin görünmesi için kritik adım.
myappid = 'resurrection-of-cheater.1.0'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# --- 2. Modül Yolu Fixi ---
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Servis İçe Aktarmaları
from services.win_api import apply_stealth_mode, SW_MINIMIZE
from services.ocr_service import OCRManager
from services.ai_service import AIManager
from config import LOCALIZATION, BASE_PATH, ICON_PATH

class SnippingTool:
    def __init__(self, master, callback):
        self.master = master
        self.callback = callback
        self.snip_surface = tk.Toplevel(master)
        self.snip_surface.attributes('-alpha', 0.3, '-fullscreen', True, "-topmost", True)
        self.canvas = tk.Canvas(self.snip_surface, cursor="cross", bg="grey")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<ButtonPress-1>", self.start_snip)
        self.canvas.bind("<B1-Motion>", self.drag_snip)
        self.canvas.bind("<ButtonRelease-1>", self.end_snip)
        self.rect = None

    def start_snip(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, 1, 1, outline='#8A2BE2', width=3)

    def drag_snip(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def end_snip(self, event):
        x1, y1 = min(self.start_x, event.x), min(self.start_y, event.y)
        w, h = abs(self.start_x - event.x), abs(self.start_y - event.y)
        self.snip_surface.destroy()
        if w > 5 and h > 5:
            self.callback(pyautogui.screenshot(region=(int(x1), int(y1), int(w), int(h))))

class CheaterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # --- 3. Pencere Başlığı ---
        # Arayüzde görünmez ama Görev Çubuğunda "CTk" yerine bu yazar.
        self.title("Resurrection of Cheater")
        
        self.ai = AIManager()
        self.ocr = OCRManager()
        
        # Pencere Özellikleri
        self.overrideredirect(True)
        self.geometry("1150x750+100+100")
        self.minsize(900, 600)
        self.configure(fg_color="#000000")

        # --- 4. İkon Yükleme ---
        if os.path.exists(ICON_PATH):
            self.iconbitmap(ICON_PATH)

        # Stealth Mode ve İkon Fixi
        self.after(200, lambda: apply_stealth_mode(self))
        
        self.purple, self.silver, self.dark_grey = "#8A2BE2", "#C0C0C0", "#1A1A1A"
        self.setup_ui()
        self.update_language("Türkçe")

        # Resize Mekanizması
        self.bind("<Button-1>", self.save_drag_origin)
        self.bind("<B1-Motion>", self.perform_resize)

    def setup_ui(self):
        # --- Title Bar ---
        self.title_bar = ctk.CTkFrame(self, fg_color=self.dark_grey, height=50, corner_radius=0)
        self.title_bar.pack(fill="x", side="top")
        self.title_label = ctk.CTkLabel(self.title_bar, text="RESURRECTION OF CHEATER", 
                                        text_color=self.purple, font=("Bodoni Moda", 20, "bold"))
        self.title_label.pack(side="left", padx=25)

        self.add_title_btn("✕", "#CC0000", self.destroy)
        self.add_title_btn("⬜", self.purple, self.toggle_fullscreen)
        self.add_title_btn("—", self.purple, self.minimize_app)
        self.add_title_btn("✂", self.purple, self.start_snipping)

        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)

        # --- Main Layout ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.left_panel = ctk.CTkFrame(self.main_container, fg_color=self.dark_grey, border_color=self.silver, border_width=1)
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=10)
        self.source_label = ctk.CTkLabel(self.left_panel, text="", text_color=self.silver, font=("Bodoni Moda", 14, "bold"))
        self.source_label.pack(pady=10)
        self.text_area = ctk.CTkTextbox(self.left_panel, fg_color="#050505", text_color=self.silver, font=("Consolas", 16), border_color=self.purple, border_width=1)
        self.text_area.pack(fill="both", expand=True, padx=15, pady=15)

        self.right_panel = ctk.CTkFrame(self.main_container, fg_color="#0A0A0A", border_color=self.purple, border_width=1)
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=10)
        self.result_label = ctk.CTkLabel(self.right_panel, text="", text_color=self.purple, font=("Consolas", 14, "italic"))
        self.result_label.pack(pady=10)
        self.result_area = ctk.CTkTextbox(self.right_panel, fg_color="#000000", text_color="#D4D4D4", font=("Consolas", 16), border_color="#333333", border_width=0)
        self.result_area.pack(fill="both", expand=True, padx=20, pady=20)
        self.result_area._textbox.configure(insertbackground=self.purple, spacing2=8)

        # Tags
        self.result_area._textbox.tag_config("h1", foreground=self.purple, font=("Consolas", 24, "bold"), spacing1=15, spacing3=10)
        self.result_area._textbox.tag_config("h2", foreground=self.silver, font=("Consolas", 19, "bold"), spacing1=12, spacing3=8)
        self.result_area._textbox.tag_config("bold", foreground="white", font=("Consolas", 16, "bold"))
        self.result_area._textbox.tag_config("list", foreground="#6A9955", lmargin1=25, lmargin2=40)
        self.result_area._textbox.tag_config("code", foreground="#CE9178", background="#1E1E1E")

        self.main_container.grid_columnconfigure((0,1), weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        # Toolbar
        self.toolbar = ctk.CTkFrame(self, fg_color="transparent")
        self.toolbar.pack(pady=20, fill="x", padx=25)
        self.lang_option = ctk.CTkOptionMenu(self.toolbar, values=list(LOCALIZATION.keys()), command=self.update_language, fg_color=self.dark_grey, button_color=self.purple)
        self.lang_option.grid(row=0, column=0, padx=15)
        self.btn_scan = ctk.CTkButton(self.toolbar, text="", fg_color=self.purple, command=self.start_snipping)
        self.btn_scan.grid(row=0, column=1, padx=15)
        self.btn_trans = ctk.CTkButton(self.toolbar, text="", fg_color=self.silver, text_color="black", command=self.translate_text)
        self.btn_trans.grid(row=0, column=2, padx=15)
        self.btn_ai = ctk.CTkButton(self.toolbar, text="", fg_color=self.purple, command=self.ask_ai)
        self.btn_ai.grid(row=0, column=3, padx=15)
        self.btn_speak = ctk.CTkButton(self.toolbar, text="", fg_color=self.silver, text_color="black", command=self.speak_text)
        self.btn_speak.grid(row=0, column=4, padx=15)

    def add_title_btn(self, text, hover, cmd):
        btn = ctk.CTkButton(self.title_bar, text=text, width=50, height=50, fg_color="transparent", hover_color=hover, font=("Consolas", 16), command=cmd)
        btn.pack(side="right")

    def render_markdown(self, raw_text):
        self.result_area.delete("0.0", "end")
        lines = raw_text.split("\n")
        for line in lines:
            line = line.strip()
            if not line: self.result_area.insert("end", "\n"); continue
            if line.startswith("# "): self.result_area.insert("end", line[2:] + "\n", "h1")
            elif line.startswith("## "): self.result_area.insert("end", line[3:] + "\n", "h2")
            elif line.startswith("- ") or line.startswith("* "): self.result_area.insert("end", " • " + line[2:] + "\n", "list")
            elif "**" in line:
                parts = line.split("**")
                for i, part in enumerate(parts):
                    if i % 2 == 1: self.result_area.insert("end", part, "bold")
                    else: self.result_area.insert("end", part)
                self.result_area.insert("end", "\n")
            elif line.startswith("```") or line.startswith("`"):
                clean_code = line.replace("```", "").replace("`", "")
                self.result_area.insert("end", " " + clean_code + " \n", "code")
            else: self.result_area.insert("end", line + "\n")

    def start_snipping(self):
        if os.path.exists(self.ocr.tesseract_cmd):
            self.withdraw()
            SnippingTool(self, self.process_screenshot)
        else: messagebox.showerror("Hata", "Tesseract-OCR bulunamadı!")

    def process_screenshot(self, img):
        self.deiconify()
        # Ekran görüntüsü döndüğünde odağı tazele
        self.after(100, lambda: apply_stealth_mode(self)) 
        
        text = self.ocr.process(img)
        
        # Editörün yazılabilir olduğundan emin oluyoruz
        self.text_area.configure(state="normal")
        self.text_area.delete("0.0", "end")
        self.text_area.insert("0.0", text)
        self.text_area.focus_set() # Otomatik odaklan

    def translate_text(self):
        content = self.text_area.get("0.0", "end").strip()
        if content:
            target = "tr" if self.lang_option.get() == "Türkçe" else "en"
            self.ai.translate(content, target, lambda res: self.after(0, lambda: self.render_markdown(f"# ÇEVİRİ SONUCU\n\n{res}")))

    def ask_ai(self):
        content = self.text_area.get('0.0', 'end').strip()
        if content:
            lang = self.lang_option.get()
            self.result_area.delete("0.0", "end")
            self.result_area.insert("end", "⏳ Analiz Başlatıldı...\n", "bold")
            self.ai.analyze(LOCALIZATION[lang]["ai_prompt"], content, lambda res: self.after(0, lambda: self.render_markdown(res)))

    def speak_text(self):
        content = self.result_area.get("0.0", "end").strip()
        if content:
            lang = "tr" if self.lang_option.get() == "Türkçe" else "en"
            clean_text = content.replace("#", "").replace("*", "").replace("•", "")
            self.ai.speak(clean_text, lang)

    def update_language(self, choice):
        lang = LOCALIZATION[choice]
        self.source_label.configure(text=lang["source"])
        self.result_label.configure(text=lang["result"])
        self.btn_scan.configure(text=lang["btn_snip"])
        self.btn_trans.configure(text=lang["btn_trans"])
        self.btn_ai.configure(text=lang["btn_ai"])
        self.btn_speak.configure(text=lang["btn_speak"])

    def minimize_app(self):
        hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
        if hwnd == 0: hwnd = self.winfo_id()
        ctypes.windll.user32.ShowWindow(hwnd, SW_MINIMIZE)

    def toggle_fullscreen(self):
        is_full = self.attributes("-fullscreen")
        self.overrideredirect(False)
        self.attributes("-fullscreen", not is_full)
        self.overrideredirect(True)
        if os.path.exists(ICON_PATH):
            self.iconbitmap(ICON_PATH)
        self.after(200, lambda: apply_stealth_mode(self))

    def start_move(self, event): self.x, self.y = event.x, event.y
    def do_move(self, event): 
        if not self.attributes("-fullscreen"):
            self.geometry(f"+{self.winfo_x()+(event.x-self.x)}+{self.winfo_y()+(event.y-self.y)}")

    def save_drag_origin(self, event):
        self.drag_start_x, self.drag_start_y = event.x_root, event.y_root
        self.drag_start_w, self.drag_start_h = self.winfo_width(), self.winfo_height()

    def perform_resize(self, event):
        if event.x > self.winfo_width() - 25 and event.y > self.winfo_height() - 25:
            new_w = max(900, self.drag_start_w + (event.x_root - self.drag_start_x))
            new_h = max(600, self.drag_start_h + (event.y_root - self.drag_start_y))
            self.geometry(f"{new_w}x{new_h}")

if __name__ == "__main__":
    app = CheaterApp()
    app.mainloop()