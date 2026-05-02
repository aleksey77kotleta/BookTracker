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

        # Логика

        def add_book(self):
            title = self.title_entry.get().strip()
            author = self.author_entry.get().strip()
            pages = self.pages_entry.get().strip()

            # Валидация
            if not title or not author or not pages:
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
                return

            if not pages.isdigit():
                messagebox.showerror("Ошибка", "В поле 'Страницы' должны быть только цифры!")
                return

            # Добавление в список
            new_book = {
                "title": title,
                "author": author,
                "pages": pages
            }
            self.books.append(new_book)

            self.save_data()
            self.update_listbox()
            self.clear_entries()
            messagebox.showinfo("Успех", f"Книга '{title}' добавлена!")

        def filter_books(self):
            query = self.search_entry.get().lower().strip()
            self.books_listbox.delete(0, tk.END)

            for book in self.books:
                if query in book['title'].lower() or query in book['author'].lower():
                    display_text = f"{book['title']} — {book['author']} ({book['pages']} стр.)"
                    self.books_listbox.insert(tk.END, display_text)

        def delete_book(self):
            try:
                # Получаем индекс выбранной строки в Listbox
                selected_index = self.books_listbox.curselection()[0]
                # Чтобы правильно удалить из основного списка при включенном фильтре,
                # находим книгу по тексту строки
                selected_text = self.books_listbox.get(selected_index)

                # Удаляем из основного списка self.books
                self.books = [b for b in self.books if
                              f"{b['title']} — {b['author']} ({b['pages']} стр.)" != selected_text]

                self.save_data()
                self.update_listbox()
            except IndexError:
                messagebox.showwarning("Внимание", "Сначала выберите книгу для удаления!")

        def get_random_book(self):
            if not self.books:
                messagebox.showwarning("Пусто", "Список книг пуст!")
                return
            book = random.choice(self.books)
            messagebox.showinfo("Рекомендация", f"Почитайте сегодня:\n\n{book['title']}\nАвтор: {book['author']}")

        def update_listbox(self):
            """Просто обновляет список, сбрасывая фильтр"""
            self.books_listbox.delete(0, tk.END)
            for book in self.books:
                self.books_listbox.insert(tk.END, f"{book['title']} — {book['author']} ({book['pages']} стр.)")

        def clear_entries(self):
            self.title_entry.delete(0, tk.END)
            self.author_entry.delete(0, tk.END)
            self.pages_entry.delete(0, tk.END)

            # Работа с JSON

        def save_data(self):
            try:
                with open(self.file_path, "w", encoding="utf-8") as f:
                    json.dump(self.books, f, ensure_ascii=False, indent=4)
            except Exception as e:
                messagebox.showerror("Ошибка сохранения",