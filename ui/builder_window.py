import tkinter as tk
from tkinter import messagebox, filedialog
from core.config_manager import save_config

class BuilderWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RunAs Config Builder")
        self.geometry("500x560")
        
        # Base font
        base_font = ("Segoe UI", 10)
        
        # User input
        tk.Label(self, text="Логін Адміністратора:", font=base_font).pack(anchor="w", padx=15, pady=(15, 2))
        self.user_input = tk.Entry(self, width=50, font=base_font)
        self.user_input.pack(fill="x", padx=15, pady=(0, 10))
        
        # Password input
        tk.Label(self, text="Пароль Адміністратора:", font=base_font).pack(anchor="w", padx=15, pady=(5, 2))
        self.pass_input = tk.Entry(self, width=50, show="*", font=base_font)
        self.pass_input.pack(fill="x", padx=15, pady=(0, 10))
        
        # Domain input
        tk.Label(self, text="Домен (ПК):", font=base_font).pack(anchor="w", padx=15, pady=(5, 2))
        self.domain_input = tk.Entry(self, width=50, font=base_font)
        self.domain_input.insert(0, ".")
        self.domain_input.pack(fill="x", padx=15, pady=(0, 10))
        
        # Commands input
        tk.Label(self, text="Команди (кожна з нового рядка):", font=base_font).pack(anchor="w", padx=15, pady=(5, 2))
        self.commands_input = tk.Text(self, width=50, height=8, font=("Consolas", 10))
        self.commands_input.pack(padx=15, pady=(0, 10), fill="both", expand=True)
        
        # Encryption Password input
        tk.Label(self, text="Пароль для шифрування файлу (майстер-пароль):", fg="#0055aa", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=15, pady=(10, 2))
        self.enc_pass_input = tk.Entry(self, width=50, show="*", font=base_font)
        self.enc_pass_input.pack(fill="x", padx=15, pady=(0, 10))
        
        # Execution mode (Sequential vs Concurrent)
        self.wait_var = tk.BooleanVar(value=True)
        self.wait_checkbox = tk.Checkbutton(
            self, 
            text="Чекати завершення кожної команди (послідовне виконання)", 
            variable=self.wait_var,
            font=base_font
        )
        self.wait_checkbox.pack(anchor="w", padx=15, pady=(0, 15))
        
        # Save button
        self.save_btn = tk.Button(self, text="Зберегти конфіг (.enc)", command=self.save_configuration, bg="#28a745", fg="white", font=("Segoe UI", 11, "bold"), relief="flat", cursor="hand2")
        self.save_btn.pack(pady=(5, 15), ipadx=10, ipady=5)
        
    def save_configuration(self):
        user = self.user_input.get().strip()
        password = self.pass_input.get()
        domain = self.domain_input.get().strip()
        enc_password = self.enc_pass_input.get()
        wait_for_completion = self.wait_var.get()
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
            "wait_for_completion": wait_for_completion,
            "commands": commands
        }
        
        filepath = filedialog.asksaveasfilename(
            title="Зберегти файл конфігурації",
            defaultextension=".enc",
            filetypes=[("Encrypted Files", "*.enc")]
        )
        if filepath:
            try:
                import os
                save_config(filepath, data, enc_password)
                
                # Create bat file next to the .enc file
                bat_path = os.path.splitext(filepath)[0] + ".bat"
                enc_filename = os.path.basename(filepath)
                
                bat_content = f'@echo off\ncd /d "%~dp0"\nstart "" "RunAsTool.exe" "{enc_filename}"\n'
                with open(bat_path, "w", encoding="cp1251") as f:
                    f.write(bat_content)
                
                messagebox.showinfo("Успіх", f"Конфігурацію успішно зашифровано та збережено у:\n{filepath}\n\nТакож поруч створено файл-запускатор:\n{os.path.basename(bat_path)}\n\nНе забудьте передати пароль шифрування кінцевому користувачу разом із RunAsTool.exe!")
                self.enc_pass_input.delete(0, tk.END) # Clear encryption password for security
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося зберегти конфіг:\n{str(e)}")
