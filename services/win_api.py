import ctypes
import os

# Windows API Sabitleri
GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
WS_EX_NOACTIVATE = 0x08000000 
SW_MINIMIZE = 6

def apply_stealth_mode(root):
    """Pencereyi Görev Çubuğuna mühürler, odağı çalmasını engeller ve barı gizler."""
    # 1. Kenarlıksız modu zorla
    root.overrideredirect(True) 
    
    hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
    if hwnd == 0: hwnd = root.winfo_id()
    
    style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    
    # 2. ToolWindow kapat, APPWINDOW (Taskbar) ve NOACTIVATE (Stealth) aç
    new_style = (style & ~0x00000080) | WS_EX_APPWINDOW | WS_EX_NOACTIVATE
    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, new_style)
    
    # 3. İkon Fix: WinAPI seviyesinde ikonun kalıcılığını sağla
    from config import ICON_PATH
    if os.path.exists(ICON_PATH):
        root.iconbitmap(ICON_PATH)
    
    # 4. Taskbar'ı yenilemek için withdraw/deiconify
    root.withdraw()
    root.after(10, root.deiconify)