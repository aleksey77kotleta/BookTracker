import tkinter as tk
from tkinter import messagebox
import json
import random

class BookTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.root.geometry("450x650")

        # Данные
        self.books = []
        self.file_path = "data.json"
        self.load_data()

        # Ввод данных
        tk.Label(root, text="Название книги:", font=('Arial', 10, 'bold')).pack(pady=(10, 0))
        self.title_entry = tk.Entry(root, width=40)
        self.title_entry.pack(pady=5)

        tk.Label(root, text="Автор:", font=('Arial', 10, 'bold')).pack(pady=(10, 0))
        self.author_entry = tk.Entry(root, width=40)
        self.author_entry.pack(pady=5)

        tk.Label(root, text="Количество страниц:", font=('Arial', 10, 'bold')).pack(pady=(10, 0))
        self.pages_entry = tk.Entry(root, width=40)
        self.pages_entry.pack(pady=5)

        # Кнопки
        tk.Button(root, text="Добавить книгу", command=self.add_book, bg="#4CAF50", fg="white", width=20).pack(pady=10)
        tk.Button(root, text="Случайная книга", command=self.get_random_book, width=20).pack(pady=5)

        # Интерфейс
        tk.Label(root, text="Поиск по названию или автору:", font=('Arial', 10, 'italic')).pack(pady=(20, 0))
        self.search_entry = tk.Entry(root, width=40)
        self.search_entry.pack(pady=5)
        # Привязываем фильтрацию на лету при каждом нажатии клавиши
        self.search_entry.bind("<KeyRelease>", lambda event: self.filter_books())

        self.books_listbox = tk.Listbox(root, width=50, height=10)
        self.books_listbox.pack(pady=10, padx=20)

        tk.Button(root, text="Удалить выбранную", command=self.delete_book, bg="#f44336", fg="white").pack(pady=5)

        # Отображаем данные при запуске
        self.update_listbox()