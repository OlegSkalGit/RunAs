import sys
import tkinter as tk
from tkinter import messagebox, simpledialog
from ui.builder_window import BuilderWindow
from ui.progress_window import ProgressWindow
from core.config_manager import load_config

def main():
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
        
        # Init hidden root for dialogs
        root = tk.Tk()
        root.withdraw()
        
        # Ask user for the decryption password
        enc_password = simpledialog.askstring("Дешифрування", "Введіть пароль для розшифрування файлу:", show='*')
        if not enc_password:
            # User canceled or entered empty password
            sys.exit(0)
            
        try:
            config_data = load_config(config_path, enc_password)
            app = ProgressWindow(config_data)
            app.mainloop()
        except Exception as e:
            messagebox.showerror("Помилка доступу", str(e))
            sys.exit(1)
    else:
        app = BuilderWindow()
        app.mainloop()

if __name__ == "__main__":
    main()
