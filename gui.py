import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from classes import Task, TaskManager

class TaskManagerApp:
    def __init__(self, root: tk.Tk):
        self.manager = TaskManager()
        self.root = root
        self.root.title("Менеджер задач")
        self.root.geometry("600x520")
        self.root.minsize(550, 480)

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.setup_ui()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        input_frame = ttk.LabelFrame(main_frame, text=" Новая задача ", padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky="w", pady=2)
        self.title_entry = ttk.Entry(input_frame, width=40)
        self.title_entry.grid(row=0, column=1, columnspan=2, sticky="ew", pady=2, padx=5)

        ttk.Label(input_frame, text="Срок (ГГГГ-ММ-ДД):").grid(row=1, column=0, sticky="w", pady=2)
        self.date_entry = ttk.Entry(input_frame, width=15)
        self.date_entry.grid(row=1, column=1, sticky="w", pady=2, padx=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        ttk.Label(input_frame, text="Описание:").grid(row=2, column=0, sticky="nw", pady=2)
        self.desc_text = tk.Text(input_frame, height=3, width=35, font=("TkDefaultFont", 9))
        self.desc_text.grid(row=2, column=1, columnspan=2, sticky="ew", pady=2, padx=5)

        input_frame.columnconfigure(1, weight=1)

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 10))

        add_btn = ttk.Button(btn_frame, text="✚ Добавить задачу", command=self.add_task)
        add_btn.pack(side=tk.LEFT, padx=(0, 5))

        del_btn = ttk.Button(btn_frame, text="✖ Удалить выбранную", command=self.delete_task)
        del_btn.pack(side=tk.LEFT)

        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)

        list_container = ttk.Frame(content_frame)
        list_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        ttk.Label(list_container, text="Список задач:").pack(anchor="w")
        
        scroll = ttk.Scrollbar(list_container)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tasks_listbox = tk.Listbox(
            list_container, 
            selectmode=tk.SINGLE, 
            yscrollcommand=scroll.set,
            font=("TkDefaultFont", 10),
            activestyle="none"
        )
        self.tasks_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.config(command=self.tasks_listbox.yview)

        self.tasks_listbox.bind("<<ListboxSelect>>", self.show_task_details)

        details_frame = ttk.LabelFrame(content_frame, text=" Детали ", padding="10")
        details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.details_label = ttk.Label(details_frame, text="Выберите задачу для просмотра", wraplength=200, justify="left")
        self.details_label.pack(anchor="nw")

        self.update_listbox()

    def add_task(self):
        title = self.title_entry.get()
        description = self.desc_text.get("1.0", tk.END)
        due_date = self.date_entry.get()

        if not title.strip() or not due_date.strip():
            messagebox.showwarning("Внимание", "Заполните название и дату!")
            return

        try:
            task = Task(title, description, due_date)
            self.manager.add_task(task)
            self.update_listbox()
            self.clear_inputs()
        except ValueError as e:
            messagebox.showerror("Ошибка в дате", str(e))

    def delete_task(self):
        selected = self.tasks_listbox.curselection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите задачу из списка!")
            return

        idx = selected[0]
        self.manager.delete_task(idx)
        self.update_listbox()
        self.details_label.config(text="Выберите задачу для просмотра")

    def show_task_details(self, event=None):
        selected = self.tasks_listbox.curselection()
        if selected:
            task = self.manager.tasks[selected[0]]
            text = f"📌 {task.title}\n\n📅 Срок: {task.due_date}\n\n📝 Описание:\n{task.description or 'Без описания'}"
            self.details_label.config(text=text)

    def update_listbox(self):
        self.tasks_listbox.delete(0, tk.END)
        for task in self.manager.tasks:
            self.tasks_listbox.insert(tk.END, f"{task.title}  [{task.due_date}]")

    def clear_inputs(self):
        self.title_entry.delete(0, tk.END)
        self.desc_text.delete("1.0", tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()