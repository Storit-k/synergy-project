import tkinter as tk
from tkinter import ttk
import sqlite3


# класс главного окна
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.db = db
        self._init_main()

    # Инициализация объектов
    def _init_main(self):
        toolbar = tk.Frame(self, background='#7a7a85', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Изображения
        self.add_img = tk.PhotoImage(file='./img/add.png')
        self.update_img = tk.PhotoImage(file='./img/update.png')
        self.delete_img = tk.PhotoImage(file='./img/delete.png')
        self.search_img = tk.PhotoImage(file='./img/search.png')
        self.refresh_img = tk.PhotoImage(file='./img/refresh.png')

        # Добавления кнопок
        open_dialog_button = tk.Button(toolbar, background='#7f7f87', bd=0, command=self.open_dialog,
                                       image=self.add_img)
        open_dialog_button.pack(side=tk.LEFT)
        edit_dialog_button = tk.Button(toolbar, background='#7f7f87', bd=0, command=self.open_update_dialog,
                                       image=self.update_img)
        edit_dialog_button.pack(side=tk.LEFT)
        delete_button = tk.Button(toolbar, background='#7f7f87', bd=0, command=self.delete_record,
                                  image=self.delete_img)
        delete_button.pack(side=tk.LEFT)
        search_button = tk.Button(toolbar, background='#7f7f87', bd=0, command=self.open_search_dialog,
                                  image=self.search_img)
        search_button.pack(side=tk.LEFT)
        refresh_button = tk.Button(toolbar, background='#7f7f87', bd=0, command=self.view_records,
                                   image=self.refresh_img)
        refresh_button.pack(side=tk.LEFT)

        # Добавление Treeview
        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'tel', 'email'), height=45, show='headings')
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('tel', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('tel', text='Телефон')
        self.tree.heading('email', text='E-mail')

        self.tree.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

        self.view_records()

    # Вызов дочернего окна
    def open_dialog(self):
        Child()

    # Вызов окна для изменения данных
    def open_update_dialog(self):
        Update()

    # Вызов окна поиска
    def open_search_dialog(self):
        Search()

    # Запись данных в БД
    def records(self, name, phone, email):
        self.db.insert_data(name, phone, email)
        self.view_records()

    # Обновление данных
    def update_record(self, name, phone, email):
        self.db.c.execute("UPDATE db SET name=?, phone=?, email=? WHERE ID=?", (name, phone, email,
                          self.tree.set(self.tree.selection()[0], '#1')))
        self.db.commit()
        self.view_records()

    # Удаление записей
    def delete_record(self):
        for selected_item in self.tree.selection():
            self.db.c.execute("DELETE FROM db WHERE ID=?", (self.tree.set(selected_item, '#1'),))
        self.db.commit()
        self.view_records()

    # Поиск записей
    def search_record(self, name):
        name = f'%{name}%'
        self.db.c.execute("SELECT * FROM db WHERE name LIKE ?", (name,))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    # Вывод данных в Treeview
    def view_records(self):
        self.db.c.execute('SELECT * FROM db')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

        if len(children := self.tree.get_children()) != 0:
            self.tree.selection_set(children[0])


# Класс дочерних окон
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.view = app
        self._init_child()

    def _init_child(self):
        # Насройка окна
        self.title('Добавить')
        self.geometry('400x220')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        # Подписи
        self.label_name = tk.Label(self, text='ФИО:')
        self.label_name.place(x=50, y=50)
        self.label_phone = tk.Label(self, text='Телефон:')
        self.label_phone.place(x=50, y=80)
        self.label_email = tk.Label(self, text='E-mail:')
        self.label_email.place(x=50, y=110)

        # Поля ввода данных
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x=200, y=80)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=110)

        # Кнопки взаимодействия
        self.close_button = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.close_button.place(x=300, y=170)
        self.add_button = ttk.Button(self, text='Добавить', command=lambda: self.view.records(self.entry_name.get(),
                                     self.entry_phone.get(), self.entry_email.get()))
        self.add_button.place(x=220, y=170)


# Окно для обновления
class Update(Child):
    def __init__(self):
        super().__init__()
        self._init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def _init_edit(self):
        self.title('Редактировать позицию')

        edit_button = ttk.Button(self, text='Редактировать')
        edit_button.bind('<Button-1>', lambda event: self.view.update_record(self.entry_name.get(),
                                                                             self.entry_phone.get(),
                                                                             self.entry_email.get()))
        edit_button.bind('<Button-1>', lambda event: self.destroy(), add='+')
        edit_button.place(x=205, y=170)

        self.add_button.destroy()

    def default_data(self):
        db.c.execute("""SELECT * FROM db WHERE ID=?""", self.view.tree.set(self.view.tree.selection()[0], '#1'))
        row = db.c.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])


# Окно для поиска записей
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self._init_search()
        self.view = app

    def _init_search(self):
        self.title('Поиск')
        self.geometry('300x100')
        self.resizable(False, False)

        search_label = tk.Label(self, text='Поиск')
        search_label.place(x=50, y=20)

        search_entry = ttk.Entry(self)
        search_entry.place(x=105, y=20, width=150)

        cansel_button = ttk.Button(self, text='Закрыть', command=self.destroy)
        cansel_button.place(x=185, y=50)

        search_button = ttk.Button(self, text='Поиск', command=lambda: self.view.search_record(search_entry.get())
                                   or self.destroy())
        search_button.place(x=105, y=50)


# Класс БД (наследуется от класса Connection из sqlite3)
class DB(sqlite3.Connection):
    def __init__(self):
        super().__init__('db.db')
        self.c = self.cursor()

        self.c.execute("""
            CREATE TABLE IF NOT EXISTS db(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL
            )""")
        self.commit()

    def insert_data(self, name, phone, email):
        self.c.execute("INSERT INTO db (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
        self.commit()


if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Телефонная книга')
    root.geometry('665x450')
    root.resizable(False, False)
    root.mainloop()