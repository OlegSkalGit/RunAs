import tkinter as tk
from tkinter import messagebox, filedialog
from core.config_manager import save_config

class BuilderWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RunAs Config Builder")
        self.geometry("500x480")
        
        # User input
        tk.Label(self, text="Логін (Admin):").pack(anchor="w", padx=10, pady=(10, 0))
        self.user_input = tk.Entry(self, width=50)
        self.user_input.pack(padx=10, pady=2)
        
        # Password input
        tk.Label(self, text="Пароль Адміністратора:").pack(anchor="w", padx=10, pady=(5, 0))
        self.pass_input = tk.Entry(self, width=50, show="*")
        self.pass_input.pack(padx=10, pady=2)
        
        # Domain input
        tk.Label(self, text="Домен (ПК):").pack(anchor="w", padx=10, pady=(5, 0))
        self.domain_input = tk.Entry(self, width=50)
        self.domain_input.insert(0, ".")
        self.domain_input.pack(padx=10, pady=2)
        
        # Commands input
        tk.Label(self, text="Команди (кожна з нового рядка):").pack(anchor="w", padx=10, pady=(5, 0))
        self.commands_input = tk.Text(self, width=50, height=8)
        self.commands_input.pack(padx=10, pady=2, fill="both", expand=True)
        
        # Encryption Password input
        tk.Label(self, text="Пароль для шифрування файлу (майстер-пароль):", fg="blue").pack(anchor="w", padx=10, pady=(10, 0))
        self.enc_pass_input = tk.Entry(self, width=50, show="*")
        self.enc_pass_input.pack(padx=10, pady=2)
        
        # Save button
        self.save_btn = tk.Button(self, text="Зберегти конфіг (.enc)", command=self.save_configuration, bg="green", fg="white", font=("Arial", 10, "bold"))
        self.save_btn.pack(pady=15)
        
    def save_configuration(self):
        user = self.user_input.get().strip()
        password = self.pass_input.get()
        domain = self.domain_input.get().strip()
        enc_password = self.enc_pass_input.get()
        commands_text = self.commands_input.get("1.0", tk.END)
        commands = [cmd.strip() for cmd in commands_text.split('\n') if cmd.strip()]
        
        if not user or not password or not commands:
            messagebox.showwarning("Помилка", "Заповніть логін, пароль адміністратора та хоча б одну команду!")
            return
            
        if not enc_password:
            messagebox.showwarning("Помилка", "Обов'язково вкажіть пароль для шифрування файлу (він знадобиться при запуску)!")
            return
            
        data = {
            "username": user,
            "password": password,
            "domain": domain,
            "commands": commands
        }
        
        filepath = filedialog.asksaveasfilename(
            title="Зберегти файл конфігурації",
            defaultextension=".enc",
            filetypes=[("Encrypted Files", "*.enc")]
        )
        if filepath:
            try:
                save_config(filepath, data, enc_password)
                messagebox.showinfo("Успіх", f"Конфігурацію успішно зашифровано та збережено у:\n{filepath}\n\nНе забудьте передати пароль шифрування кінцевому користувачу!")
                self.enc_pass_input.delete(0, tk.END) # Clear encryption password for security
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося зберегти конфіг:\n{str(e)}")
