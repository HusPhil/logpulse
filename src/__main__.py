# src/__main__.py
import tkinter as tk
import threading
from tray import run_tray
from gui import show_popup

root = tk.Tk()
root.withdraw()

threading.Thread(target=run_tray, args=(root,), daemon=True).start()

# Schedule first popup after some interval
root.after(60000, lambda: show_popup(root))
root.mainloop()
