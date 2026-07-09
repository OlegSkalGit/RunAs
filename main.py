import sys
import tkinter as tk
from tkinter import messagebox
from ui.builder_window import BuilderWindow
from ui.progress_window import ProgressWindow
from core.config_manager import load_config

def main():
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
        try:
            config_data = load_config(config_path)
            app = ProgressWindow(config_data)
            app.mainloop()
        except Exception as e:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Помилка", f"Не вдалося завантажити конфігурацію:\n{e}")
            sys.exit(1)
    else:
        app = BuilderWindow()
        app.mainloop()

if __name__ == "__main__":
    main()
