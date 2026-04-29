import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import webbrowser

from PIL import Image, ImageTk


class GraphicEditorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Графічний редактор")
        self.root.geometry("1100x750")

        self.current_tool = tk.StringVar(value="Олівець")
        self.toolbar_visible = tk.BooleanVar(value=True)

        self.image_width = 1600
        self.image_height = 1200
        self.image = Image.new("RGB", (self.image_width, self.image_height), "white")
        self.photo_image = None
        self.canvas_image_id = None

        self._create_menu()
        self._create_toolbar()
        self._create_canvas_area()
        self._create_status_bar()
        self._refresh_canvas_image()

    def _create_menu(self):
        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Новий", command=self._not_implemented)
        file_menu.add_command(label="Відкрити", command=self._not_implemented)
        file_menu.add_command(label="Зберегти", command=self._not_implemented)
        file_menu.add_command(label="Зберегти як", command=self._not_implemented)
        file_menu.add_separator()
        file_menu.add_command(label="Вийти", command=self.root.quit)
        menu_bar.add_cascade(label="Файл", menu=file_menu)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Скасувати", command=self._not_implemented)
        edit_menu.add_command(label="Копіювати", command=self._not_implemented)
        edit_menu.add_command(label="Вставити", command=self._not_implemented)
        edit_menu.add_command(label="Очистити", command=self._not_implemented)
        menu_bar.add_cascade(label="Редагування", menu=edit_menu)

        tools_menu = tk.Menu(menu_bar, tearoff=0)
        tools_menu.add_command(label="Олівець", command=lambda: self._set_tool("Олівець"))
        tools_menu.add_command(label="Лінія", command=lambda: self._set_tool("Лінія"))
        tools_menu.add_command(label="Прямокутник", command=lambda: self._set_tool("Прямокутник"))
        tools_menu.add_command(label="Еліпс", command=lambda: self._set_tool("Еліпс"))
        tools_menu.add_command(label="Виокремити", command=lambda: self._set_tool("Виокремити"))
        menu_bar.add_cascade(label="Інструменти", menu=tools_menu)

        image_menu = tk.Menu(menu_bar, tearoff=0)
        image_menu.add_command(label="Відтінки сірого", command=self._not_implemented)
        image_menu.add_command(label="Інверсія кольорів", command=self._not_implemented)
        image_menu.add_command(label="Повернути на 90°", command=self._not_implemented)
        image_menu.add_command(label="Віддзеркалити горизонтально", command=self._not_implemented)
        image_menu.add_command(label="Віддзеркалити вертикально", command=self._not_implemented)
        menu_bar.add_cascade(label="Зображення", menu=image_menu)

        view_menu = tk.Menu(menu_bar, tearoff=0)
        view_menu.add_checkbutton(
            label="Показати панель інструментів",
            variable=self.toolbar_visible,
            command=self._toggle_toolbar,
        )
        menu_bar.add_cascade(label="Вигляд", menu=view_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Довідка", command=self._open_help)
        help_menu.add_command(label="Про програму", command=self._show_about)
        menu_bar.add_cascade(label="Довідка", menu=help_menu)

        self.root.config(menu=menu_bar)

    def _create_toolbar(self):
        self.toolbar_frame = tk.Frame(self.root, bd=1, relief=tk.RAISED, padx=6, pady=4)
        self.toolbar_frame.pack(side=tk.TOP, fill=tk.X)

        file_group = tk.LabelFrame(self.toolbar_frame, text="Файл", padx=4, pady=3)
        file_group.pack(side=tk.LEFT, padx=4)
        tk.Button(file_group, text="Новий", command=self._not_implemented).pack(side=tk.LEFT, padx=2)
        tk.Button(file_group, text="Відкрити", command=self._not_implemented).pack(side=tk.LEFT, padx=2)
        tk.Button(file_group, text="Зберегти", command=self._not_implemented).pack(side=tk.LEFT, padx=2)

        tools_group = tk.LabelFrame(self.toolbar_frame, text="Інструменти", padx=4, pady=3)
        tools_group.pack(side=tk.LEFT, padx=4)
        tk.Button(tools_group, text="Олівець", command=lambda: self._set_tool("Олівець")).pack(side=tk.LEFT, padx=2)
        tk.Button(tools_group, text="Лінія", command=lambda: self._set_tool("Лінія")).pack(side=tk.LEFT, padx=2)
        tk.Button(tools_group, text="Прямокутник", command=lambda: self._set_tool("Прямокутник")).pack(side=tk.LEFT, padx=2)
        tk.Button(tools_group, text="Еліпс", command=lambda: self._set_tool("Еліпс")).pack(side=tk.LEFT, padx=2)

        edit_group = tk.LabelFrame(self.toolbar_frame, text="Редагування", padx=4, pady=3)
        edit_group.pack(side=tk.LEFT, padx=4)
        tk.Button(edit_group, text="Скасувати", command=self._not_implemented).pack(side=tk.LEFT, padx=2)
        tk.Button(edit_group, text="Копіювати", command=self._not_implemented).pack(side=tk.LEFT, padx=2)
        tk.Button(edit_group, text="Вставити", command=self._not_implemented).pack(side=tk.LEFT, padx=2)

    def _create_canvas_area(self):
        canvas_frame = tk.Frame(self.root)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(canvas_frame, bg="#d9d9d9")

        h_scroll = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        v_scroll = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)

        self.canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")

        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)

    def _create_status_bar(self):
        status_frame = tk.Frame(self.root, bd=1, relief=tk.SUNKEN)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_label = tk.Label(
            status_frame,
            text=f"Поточний інструмент: {self.current_tool.get()}",
            anchor="w",
            padx=8,
            pady=4,
        )
        self.status_label.pack(fill=tk.X)

    def _refresh_canvas_image(self):
        self.photo_image = ImageTk.PhotoImage(self.image)
        if self.canvas_image_id is None:
            self.canvas_image_id = self.canvas.create_image(0, 0, image=self.photo_image, anchor="nw")
        else:
            self.canvas.itemconfig(self.canvas_image_id, image=self.photo_image)
        self.canvas.config(scrollregion=(0, 0, self.image_width, self.image_height))

    def _set_tool(self, tool_name: str):
        self.current_tool.set(tool_name)
        self.status_label.config(text=f"Поточний інструмент: {tool_name}")

    def _toggle_toolbar(self):
        if self.toolbar_visible.get():
            self.toolbar_frame.pack(side=tk.TOP, fill=tk.X)
        else:
            self.toolbar_frame.pack_forget()

    def _open_help(self):
        help_path = Path(__file__).with_name("help.html")
        if help_path.exists():
            webbrowser.open(help_path.resolve().as_uri())
        else:
            messagebox.showerror("Помилка", "Файл довідки не знайдено.")

    def _show_about(self):
        messagebox.showinfo(
            "Про програму",
            "Графічний редактор\n\n"
            "Навчальний проєкт з системного програмування.\n"
            "Поточна версія містить базову структуру застосунку.",
        )

    def _not_implemented(self):
        messagebox.showinfo("Інформація", "Ця функція буде реалізована на наступних етапах.")


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphicEditorApp(root)
    root.mainloop()
