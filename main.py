import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os

HISTORY_FILE = "history.json"

# --- Работа с историей ---
def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_history():
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

history = load_history()

# --- Генерация пароля ---
def generate_password():
    length = length_var.get()

    # Проверка длины
    if length < 4 or length > 32:
        messagebox.showerror("Ошибка", "Длина должна быть от 4 до 32")
        return

    chars = ""
    if digits_var.get():
        chars += string.digits
    if letters_var.get():
        chars += string.ascii_letters
    if symbols_var.get():
        chars += string.punctuation

    # Проверка выбора символов
    if not chars:
        messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов")
        return

    password = ''.join(random.choice(chars) for _ in range(length))
    result_var.set(password)

    # Сохранение
    history.append(password)
    save_history()
    update_table()

# --- Обновление таблицы ---
def update_table():
    for row in table.get_children():
        table.delete(row)

    for i, pwd in enumerate(history):
        table.insert("", "end", values=(i + 1, pwd))

# --- Очистка истории ---
def clear_history():
    if messagebox.askyesno("Подтверждение", "Очистить историю?"):
        history.clear()
        save_history()
        update_table()

# --- GUI ---
root = tk.Tk()
root.title("Random Password Generator")
root.geometry("400x500")

# Длина
tk.Label(root, text="Длина пароля").pack()
length_var = tk.IntVar(value=8)
tk.Scale(root, from_=4, to=32, orient="horizontal", variable=length_var).pack()

# Чекбоксы
digits_var = tk.BooleanVar(value=True)
letters_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=False)

tk.Checkbutton(root, text="Цифры", variable=digits_var).pack()
tk.Checkbutton(root, text="Буквы", variable=letters_var).pack()
tk.Checkbutton(root, text="Спецсимволы", variable=symbols_var).pack()

# Кнопки
tk.Button(root, text="Сгенерировать", command=generate_password).pack(pady=5)
tk.Button(root, text="Очистить историю", command=clear_history).pack(pady=5)

# Результат
result_var = tk.StringVar()
tk.Entry(root, textvariable=result_var, width=30, justify="center").pack(pady=10)

# Таблица
table = ttk.Treeview(root, columns=("№", "Пароль"), show="headings", height=10)
table.heading("№", text="№")
table.heading("Пароль", text="Пароль")
table.pack(fill="both", expand=True)

update_table()

root.mainloop()