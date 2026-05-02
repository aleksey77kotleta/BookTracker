# Импорт библиотек
import tkinter as tk
from tkinter import messagebox, ttk
import json
import os


class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.root.geometry("600x500")

        self.books = []
        self.file_path = "books.json"
        self.load_data()

        # Поля ввода
        frame_input = tk.Frame(self.root, padx=10, pady=10)
        frame_input.pack(fill="x")

        tk.Label(frame_input, text="Название:").grid(row=0, column=0, sticky="w")
        self.ent_title = tk.Entry(frame_input)
        self.ent_title.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(frame_input, text="Автор:").grid(row=1, column=0, sticky="w")
        self.ent_author = tk.Entry(frame_input)
        self.ent_author.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(frame_input, text="Жанр:").grid(row=2, column=0, sticky="w")
        self.ent_genre = tk.Entry(frame_input)
        self.ent_genre.grid(row=2, column=1, padx=5, pady=2)

        tk.Label(frame_input, text="Страниц:").grid(row=3, column=0, sticky="w")
        self.ent_pages = tk.Entry(frame_input)
        self.ent_pages.grid(row=3, column=1, padx=5, pady=2)

        btn_add = tk.Button(frame_input, text="Добавить книгу", command=self.add_book)
        btn_add.grid(row=4, column=0, columnspan=2, pady=10)

        # Фильтрация
        frame_filter = tk.LabelFrame(self.root, text="Фильтрация", padx=10, pady=5)
        frame_filter.pack(fill="x", padx=10)

        tk.Label(frame_filter, text="Жанр:").grid(row=0, column=0)
        self.filter_genre = tk.Entry(frame_filter, width=10)
        self.filter_genre.grid(row=0, column=1, padx=5)

        tk.Label(frame_filter, text="Мин. страниц:").grid(row=0, column=2)
        self.filter_pages = tk.Entry(frame_filter, width=5)
        self.filter_pages.grid(row=0, column=3, padx=5)

        btn_filter = tk.Button(frame_filter, text="Применить", command=self.update_table)
        btn_filter.grid(row=0, column=4, padx=5)

        # Таблица
        self.tree = ttk.Treeview(self.root, columns=("Title", "Author", "Genre", "Pages"), show='headings')
        self.tree.heading("Title", text="Название")
        self.tree.heading("Author", text="Автор")
        self.tree.heading("Genre", text="Жанр")
        self.tree.heading("Pages", text="Страниц")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.update_table()

    def add_book(self):
        title = self.ent_title.get().strip()
        author = self.ent_author.get().strip()
        genre = self.ent_genre.get().strip()
        pages = self.ent_pages.get().strip()

        # Валидация
        if not (title and author and genre and pages):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        if not pages.isdigit():
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
            return

        new_book = {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": int(pages)
        }

        self.books.append(new_book)
        self.save_data()
        self.update_table()

        # Очистка полей
        for entry in (self.ent_title, self.ent_author, self.ent_genre, self.ent_pages):
            entry.delete(0, tk.END)

    def update_table(self):
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        f_genre = self.filter_genre.get().lower()
        f_pages = self.filter_pages.get()
        min_pages = int(f_pages) if f_pages.isdigit() else 0

        for book in self.books:
            if f_genre in book['genre'].lower() and book['pages'] >= min_pages:
                self.tree.insert("", tk.END, values=(book['title'], book['author'], book['genre'], book['pages']))

    def save_data(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.books = json.load(f)


if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()
