import tkinter as tk
from pathlib import Path
import webbrowser

from PIL import Image, ImageDraw, ImageTk
from tkinter import colorchooser, messagebox


class GraphicEditorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Графічний редактор")
        self.root.geometry("1100x750")

        self.current_tool = tk.StringVar(value="Олівець")
        self.toolbar_visible = tk.BooleanVar(value=True)

        self.line_color = "#000000"
        self.fill_color = ""
        self.line_width = tk.IntVar(value=2)

        self.image_width = 1600
        self.image_height = 1200
        self.image = Image.new("RGB", (self.image_width, self.image_height), "white")
        self.photo_image = None
        self.canvas_image_id = None

        self.undo_stack = []
        self.preview_item_id = None
        self.start_x = None
        self.start_y = None
        self.last_x = None
        self.last_y = None
        self.is_drawing = False

        self._create_menu()
        self._create_toolbar()
        self._create_canvas_area()
        self._create_status_bar()
        self._bind_events()
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
        edit_menu.add_command(label="Скасувати", command=self._undo)
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

        tools_group = tk.LabelFrame(self.toolbar_frame, text="Інструменти", padx=4, pady=3)
        tools_group.pack(side=tk.LEFT, padx=4)
        tk.Button(tools_group, text="Олівець", command=lambda: self._set_tool("Олівець")).pack(side=tk.LEFT, padx=2)
        tk.Button(tools_group, text="Лінія", command=lambda: self._set_tool("Лінія")).pack(side=tk.LEFT, padx=2)
        tk.Button(tools_group, text="Прямокутник", command=lambda: self._set_tool("Прямокутник")).pack(side=tk.LEFT, padx=2)
        tk.Button(tools_group, text="Еліпс", command=lambda: self._set_tool("Еліпс")).pack(side=tk.LEFT, padx=2)

        params_group = tk.LabelFrame(self.toolbar_frame, text="Параметри", padx=4, pady=3)
        params_group.pack(side=tk.LEFT, padx=4)
        tk.Button(params_group, text="Колір лінії", command=self._choose_line_color).pack(side=tk.LEFT, padx=2)
        tk.Button(params_group, text="Колір заливки", command=self._choose_fill_color).pack(side=tk.LEFT, padx=2)
        tk.Label(params_group, text="Товщина:").pack(side=tk.LEFT, padx=(8, 2))
        tk.Spinbox(params_group, from_=1, to=20, width=4, textvariable=self.line_width).pack(side=tk.LEFT)

        edit_group = tk.LabelFrame(self.toolbar_frame, text="Редагування", padx=4, pady=3)
        edit_group.pack(side=tk.LEFT, padx=4)
        tk.Button(edit_group, text="Скасувати", command=self._undo).pack(side=tk.LEFT, padx=2)

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

        self.status_label = tk.Label(status_frame, text="", anchor="w", padx=8, pady=4)
        self.status_label.pack(fill=tk.X)
        self._update_status()

    def _update_status(self):
        self.status_label.config(
            text=(
                f"Поточний інструмент: {self.current_tool.get()} | "
                f"Колір лінії: {self.line_color} | "
                f"Товщина: {self.line_width.get()}"
            )
        )

    def _bind_events(self):
        self.canvas.bind("<ButtonPress-1>", self._on_mouse_down)
        self.canvas.bind("<B1-Motion>", self._on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self._on_mouse_up)

        self.root.bind("<Control-z>", self._undo_shortcut)
        self.root.bind("<Control-Z>", self._undo_shortcut)
        self.root.bind("<Escape>", self._cancel_preview)

    def _get_canvas_coordinates(self, event):
        return int(self.canvas.canvasx(event.x)), int(self.canvas.canvasy(event.y))

    def _refresh_canvas_image(self):
        self.photo_image = ImageTk.PhotoImage(self.image)
        if self.canvas_image_id is None:
            self.canvas_image_id = self.canvas.create_image(0, 0, image=self.photo_image, anchor="nw")
        else:
            self.canvas.itemconfig(self.canvas_image_id, image=self.photo_image)
        self.canvas.config(scrollregion=(0, 0, self.image_width, self.image_height))

    def _set_tool(self, tool_name: str):
        self.current_tool.set(tool_name)
        self._cancel_preview()
        self._update_status()

    def _toggle_toolbar(self):
        if self.toolbar_visible.get():
            self.toolbar_frame.pack(side=tk.TOP, fill=tk.X)
        else:
            self.toolbar_frame.pack_forget()

    def _choose_line_color(self):
        color = colorchooser.askcolor(title="Виберіть колір лінії", color=self.line_color)
        if color[1]:
            self.line_color = color[1]
            self._update_status()

    def _choose_fill_color(self):
        color = colorchooser.askcolor(title="Виберіть колір заливки")
        if color[1]:
            self.fill_color = color[1]

    def _save_state_for_undo(self):
        self.undo_stack.append(self.image.copy())

    def _undo(self):
        if not self.undo_stack:
            messagebox.showinfo("Інформація", "Немає дії для скасування.")
            return
        self.image = self.undo_stack.pop()
        self._refresh_canvas_image()

    def _undo_shortcut(self, event):
        self._undo()

    def _on_mouse_down(self, event):
        x, y = self._get_canvas_coordinates(event)
        self.start_x, self.start_y = x, y
        self.last_x, self.last_y = x, y
        self.is_drawing = True

        if self.current_tool.get() == "Олівець":
            self._save_state_for_undo()

    def _on_mouse_move(self, event):
        if not self.is_drawing:
            return

        x, y = self._get_canvas_coordinates(event)
        tool = self.current_tool.get()

        if tool == "Олівець":
            draw = ImageDraw.Draw(self.image)
            draw.line((self.last_x, self.last_y, x, y), fill=self.line_color, width=self.line_width.get())
            self.last_x, self.last_y = x, y
            self._refresh_canvas_image()
            return

        if tool not in {"Лінія", "Прямокутник", "Еліпс"}:
            return

        if self.preview_item_id is not None:
            self.canvas.delete(self.preview_item_id)

        if tool == "Лінія":
            self.preview_item_id = self.canvas.create_line(
                self.start_x, self.start_y, x, y, fill=self.line_color, width=self.line_width.get()
            )
        elif tool == "Прямокутник":
            self.preview_item_id = self.canvas.create_rectangle(
                self.start_x,
                self.start_y,
                x,
                y,
                outline=self.line_color,
                fill=self.fill_color if self.fill_color else "",
                width=self.line_width.get(),
            )
        elif tool == "Еліпс":
            self.preview_item_id = self.canvas.create_oval(
                self.start_x,
                self.start_y,
                x,
                y,
                outline=self.line_color,
                fill=self.fill_color if self.fill_color else "",
                width=self.line_width.get(),
            )

    def _on_mouse_up(self, event):
        if not self.is_drawing:
            return

        self.is_drawing = False
        x, y = self._get_canvas_coordinates(event)
        tool = self.current_tool.get()

        if tool == "Олівець":
            return

        if tool not in {"Лінія", "Прямокутник", "Еліпс"}:
            self._cancel_preview()
            return

        self._save_state_for_undo()
        draw = ImageDraw.Draw(self.image)
        xy = (self.start_x, self.start_y, x, y)

        if tool == "Лінія":
            draw.line(xy, fill=self.line_color, width=self.line_width.get())
        elif tool == "Прямокутник":
            draw.rectangle(
                xy,
                outline=self.line_color,
                fill=self.fill_color if self.fill_color else None,
                width=self.line_width.get(),
            )
        elif tool == "Еліпс":
            draw.ellipse(
                xy,
                outline=self.line_color,
                fill=self.fill_color if self.fill_color else None,
                width=self.line_width.get(),
            )

        self._cancel_preview()
        self._refresh_canvas_image()

    def _cancel_preview(self, event=None):
        self.is_drawing = False
        if self.preview_item_id is not None:
            self.canvas.delete(self.preview_item_id)
            self.preview_item_id = None

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
            "Реалізовано базові інструменти малювання.",
        )

    def _not_implemented(self):
        messagebox.showinfo("Інформація", "Ця функція буде реалізована на наступних етапах.")


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphicEditorApp(root)
    root.mainloop()
