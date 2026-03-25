import ctypes
import os

# Windows API Sabitleri
GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
# WS_EX_NOACTIVATE = 0x08000000  <-- Bu bayrak klavyeyi engellediği için devre dışı bıraktık.
SW_MINIMIZE = 6

def apply_stealth_mode(root):
    """Pencereyi Görev Çubuğuna mühürler, dekorasyonları gizler ve yazmaya izin verir."""
    root.overrideredirect(True) 
    
    hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
    if hwnd == 0: hwnd = root.winfo_id()
    
    style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    
    # NOACTIVATE bayrağını çıkardık, sadece APPWINDOW (Taskbar) aktif.
    new_style = (style & ~0x00000080) | WS_EX_APPWINDOW 
    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, new_style)
    
    from config import ICON_PATH
    if os.path.exists(ICON_PATH):
        root.iconbitmap(ICON_PATH)
    
    root.withdraw()
    root.after(10, root.deiconify)