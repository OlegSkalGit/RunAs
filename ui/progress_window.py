import tkinter as tk
from tkinter import ttk
import threading
from core.runner import run_commands_as_user
import sys

class ProgressWindow(tk.Tk):
    def __init__(self, config_data):
        super().__init__()
        self.title("RunAs Tool - Виконання")
        self.geometry("400x150")
        
        self.config_data = config_data
        
        self.label_var = tk.StringVar(value="Підготовка...")
        self.label = tk.Label(self, textvariable=self.label_var)
        self.label.pack(pady=20)
        
        self.progress = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)
        
        commands = self.config_data.get('commands', [])
        self.progress["maximum"] = len(commands)
        self.progress["value"] = 0
        
        # Start execution in a separate thread so GUI doesn't freeze
        threading.Thread(target=self.execute_commands, daemon=True).start()
        
    def execute_commands(self):
        user = self.config_data.get('username')
        password = self.config_data.get('password')
        domain = self.config_data.get('domain')
        commands = self.config_data.get('commands', [])
        wait_for_completion = self.config_data.get('wait_for_completion', True)
        
        results = []
        for i, cmd in enumerate(commands):
            # update UI in the main thread safely
            self.after(0, self.update_progress, i, f"Виконання: {cmd}")
            
            res = run_commands_as_user(user, password, domain, [cmd], wait_for_completion)
            results.extend(res)
            
            self.after(0, self.update_progress, i + 1, f"Завершено: {cmd}")
            
        self.after(0, self.on_finished, results)

    def update_progress(self, val, text):
        self.progress["value"] = val
        self.label_var.set(text)
        
    def on_finished(self, results):
        self.label_var.set("Усі команди виконано.")
        # Print results to console (if it's not a hidden window)
        for r in results:
            print(f"[{r['status']}] {r['command']}")
            
        sys.exit(0)
