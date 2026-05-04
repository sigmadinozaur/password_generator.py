import random
import string
import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("700x550")
        self.root.resizable(True, True)
        
        # Файл истории
        self.history_file = "password_history.json"
        self.history = self.load_history()
        
        # Параметры по умолчанию
        self.password_length = tk.IntVar(value=12)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_letters = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=True)
        
        self.setup_ui()
        self.update_history_display()
    
    def setup_ui(self):
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Настройки пароля
        settings_frame = ttk.LabelFrame(main_frame, text="Настройки пароля", padding="10")
        settings_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Ползунок длины пароля
        ttk.Label(settings_frame, text="Длина пароля:").grid(row=0, column=0, sticky=tk.W)
        length_scale = ttk.Scale(settings_frame, from_=4, to=50, variable=self.password_length, 
                                  orient=tk.HORIZONTAL, command=self.update_length_label)
        length_scale.grid(row=0, column=1, padx=10, sticky=(tk.W, tk.E))
        
        self.length_label = ttk.Label(settings_frame, text="12")
        self.length_label.grid(row=0, column=2)
        
        # Чекбоксы
        ttk.Checkbutton(settings_frame, text="Цифры (0-9)", variable=self.use_digits).grid(row=1, column=0, sticky=tk.W)
        ttk.Checkbutton(settings_frame, text="Буквы (A-Z, a-z)", variable=self.use_letters).grid(row=1, column=1, sticky=tk.W)
        ttk.Checkbutton(settings_frame, text="Спецсимволы (!@#$%^&*()_+=-[]{};:?/.>,<)", variable=self.use_special).grid(row=1, column=2, sticky=tk.W)
        
        # Кнопка генерации
        generate_btn = ttk.Button(settings_frame, text="Сгенерировать пароль", command=self.generate_password)
        generate_btn.grid(row=2, column=0, columnspan=3, pady=10)
        
        # Отображение сгенерированного пароля
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(main_frame, textvariable=self.password_var, font=("Courier", 12), width=40)
        password_entry.grid(row=1, column=0, columnspan=2, pady=10, padx=5, sticky=(tk.W, tk.E))
        
        # Кнопка копирования
        copy_btn = ttk.Button(main_frame, text="Копировать", command=self.copy_to_clipboard)
        copy_btn.grid(row=2, column=0, columnspan=2, pady=5)
        
        # История паролей
        history_frame = ttk.LabelFrame(main_frame, text="История паролей", padding="10")
        history_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Таблица истории
        columns = ("Дата", "Длина", "Параметры", "Пароль")
        self.tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        self.tree.column("Пароль", width=200)
        
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Кнопки управления историей
        btn_frame = ttk.Frame(history_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        ttk.Button(btn_frame, text="Очистить историю", command=self.clear_history).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Обновить", command=self.update_history_display).pack(side=tk.LEFT, padx=5)
        
        # Настройка весов для растягивания
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(0, weight=1)
    
    def update_length_label(self, event=None):
        self.length_label.config(text=str(int(self.password_length.get())))
    
    def get_characters(self):
        characters = ""
        if self.use_digits.get():
            characters += string.digits
        if self.use_letters.get():
            characters += string.ascii_letters
        if self.use_special.get():
            characters += "!@#$%^&*()_+=-[]{};:?/.>,<"
        
        return characters
    
    def generate_password(self):
        length = int(self.password_length.get())
        characters = self.get_characters()
        
        # Проверка корректности ввода
        if length < 4:
            messagebox.showerror("Ошибка", "Минимальная длина пароля - 4 символа")
            return
        
        if length > 50:
            messagebox.showerror("Ошибка", "Максимальная длина пароля - 50 символов")
            return
        
        if not characters:
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов")
            return
        
        # Генерация пароля
        password = ''.join(random.choice(characters) for _ in range(length))
        self.password_var.set(password)
        
        # Сохранение в историю
        params = []
        if self.use_digits.get(): params.append("цифры")
        if self.use_letters.get(): params.append("буквы")
        if self.use_special.get(): params.append("спецсимволы")
        
        history_entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "length": length,
            "parameters": ", ".join(params),
            "password": password
        }
        
        self.history.append(history_entry)
        self.save_history()
        self.update_history_display()
    
    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена!")
        else:
            messagebox.showwarning("Предупреждение", "Нет пароля для копирования")
    
    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def save_history(self):
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except IOError as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить историю: {e}")
    
    def update_history_display(self):
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Добавление записей (от новых к старым)
        for entry in reversed(self.history):
            self.tree.insert("", tk.END, values=(
                entry["date"],
                entry["length"],
                entry["parameters"],
                entry["password"]
            ))
    
    def clear_history(self):
        if messagebox.askyesno("Подтверждение", "Очистить всю историю паролей?"):
            self.history = []
            self.save_history()
            self.update_history_display()
            messagebox.showinfo("Успех", "История очищена")

def main():
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
