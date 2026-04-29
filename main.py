import tkinter as tk
from pathlib import Path
import webbrowser

from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageTk
from tkinter import colorchooser, filedialog, messagebox, simpledialog


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
        self.current_file_path = None
        self.is_modified = False

        self.undo_stack = []
        self.preview_item_id = None
        self.selection_preview_id = None
        self.selection_rect = None
        self.copied_fragment = None
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
        self.refresh_canvas()
        self._update_window_title()

    def _create_menu(self):
        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Новий", command=self._new_image)
        file_menu.add_command(label="Нове зображення з розміром", command=self._new_image_with_size)
        file_menu.add_command(label="Відкрити", command=self._open_image)
        file_menu.add_command(label="Зберегти", command=self._save_image)
        file_menu.add_command(label="Зберегти як", command=self._save_image_as)
        file_menu.add_separator()
        file_menu.add_command(label="Вийти", command=self._exit_app)
        menu_bar.add_cascade(label="Файл", menu=file_menu)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Скасувати", command=self._undo)
        edit_menu.add_command(label="Виокремити", command=lambda: self._set_tool("Виокремити"))
        edit_menu.add_command(label="Копіювати", command=self._copy_selection)
        edit_menu.add_command(label="Вставити", command=self._paste_selection)
        edit_menu.add_command(label="Очистити виділене", command=self._clear_selected_area)
        edit_menu.add_separator()
        edit_menu.add_command(label="Очистити полотно", command=self._clear_canvas)
        menu_bar.add_cascade(label="Редагування", menu=edit_menu)

        tools_menu = tk.Menu(menu_bar, tearoff=0)
        tools_menu.add_command(label="Олівець", command=lambda: self._set_tool("Олівець"))
        tools_menu.add_command(label="Лінія", command=lambda: self._set_tool("Лінія"))
        tools_menu.add_command(label="Прямокутник", command=lambda: self._set_tool("Прямокутник"))
        tools_menu.add_command(label="Еліпс", command=lambda: self._set_tool("Еліпс"))
        tools_menu.add_command(label="Виокремити", command=lambda: self._set_tool("Виокремити"))
        menu_bar.add_cascade(label="Інструменти", menu=tools_menu)

        image_menu = tk.Menu(menu_bar, tearoff=0)
        image_menu.add_command(label="Відтінки сірого", command=self._apply_grayscale)
        image_menu.add_command(label="Інверсія кольорів", command=self._apply_invert)
        image_menu.add_command(label="Повернути на 90° за годинниковою стрілкою", command=self._rotate_clockwise)
        image_menu.add_command(label="Повернути на 90° проти годинникової стрілки", command=self._rotate_counterclockwise)
        image_menu.add_command(label="Віддзеркалити горизонтально", command=self._mirror_horizontal)
        image_menu.add_command(label="Віддзеркалити вертикально", command=self._mirror_vertical)
        image_menu.add_command(label="Розмиття", command=self._apply_blur)
        menu_bar.add_cascade(label="Зображення", menu=image_menu)

        view_menu = tk.Menu(menu_bar, tearoff=0)
        view_menu.add_checkbutton(
            label="Показати/сховати панель інструментів",
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
        tk.Button(tools_group, text="Виокремити", command=lambda: self._set_tool("Виокремити")).pack(side=tk.LEFT, padx=2)

        params_group = tk.LabelFrame(self.toolbar_frame, text="Параметри", padx=4, pady=3)
        params_group.pack(side=tk.LEFT, padx=4)
        tk.Button(params_group, text="Колір лінії", command=self._choose_line_color).pack(side=tk.LEFT, padx=2)
        tk.Button(params_group, text="Колір заливки", command=self._choose_fill_color).pack(side=tk.LEFT, padx=2)
        tk.Label(params_group, text="Товщина:").pack(side=tk.LEFT, padx=(8, 2))
        tk.Spinbox(params_group, from_=1, to=20, width=4, textvariable=self.line_width).pack(side=tk.LEFT)

        edit_group = tk.LabelFrame(self.toolbar_frame, text="Редагування", padx=4, pady=3)
        edit_group.pack(side=tk.LEFT, padx=4)
        tk.Button(edit_group, text="Скасувати", command=self._undo).pack(side=tk.LEFT, padx=2)
        tk.Button(edit_group, text="Копіювати", command=self._copy_selection).pack(side=tk.LEFT, padx=2)
        tk.Button(edit_group, text="Вставити", command=self._paste_selection).pack(side=tk.LEFT, padx=2)
        tk.Button(edit_group, text="Очистити виділене", command=self._clear_selected_area).pack(side=tk.LEFT, padx=2)
        tk.Button(edit_group, text="Очистити полотно", command=self._clear_canvas).pack(side=tk.LEFT, padx=2)

        image_ops_group = tk.LabelFrame(self.toolbar_frame, text="Операції зображення", padx=4, pady=3)
        image_ops_group.pack(side=tk.LEFT, padx=4)
        tk.Button(image_ops_group, text="Сірий", command=self._apply_grayscale).pack(side=tk.LEFT, padx=2)
        tk.Button(image_ops_group, text="Інверсія", command=self._apply_invert).pack(side=tk.LEFT, padx=2)
        tk.Button(image_ops_group, text="↻ 90°", command=self._rotate_clockwise).pack(side=tk.LEFT, padx=2)
        tk.Button(image_ops_group, text="Розмиття", command=self._apply_blur).pack(side=tk.LEFT, padx=2)

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
        self.root.bind("<Control-n>", self._new_image_shortcut)
        self.root.bind("<Control-N>", self._new_image_shortcut)
        self.root.bind("<Control-o>", self._open_image_shortcut)
        self.root.bind("<Control-O>", self._open_image_shortcut)
        self.root.bind("<Control-s>", self._save_image_shortcut)
        self.root.bind("<Control-S>", self._save_image_shortcut)
        self.root.bind("<Escape>", self._cancel_preview)
        self.root.protocol("WM_DELETE_WINDOW", self._exit_app)

    def _get_canvas_coordinates(self, event):
        return int(self.canvas.canvasx(event.x)), int(self.canvas.canvasy(event.y))

    def refresh_canvas(self):
        self.image_width, self.image_height = self.image.size
        self.photo_image = ImageTk.PhotoImage(self.image)
        if self.canvas_image_id is None:
            self.canvas_image_id = self.canvas.create_image(0, 0, image=self.photo_image, anchor="nw")
        else:
            self.canvas.itemconfig(self.canvas_image_id, image=self.photo_image)
        self.canvas.tag_lower(self.canvas_image_id)
        self.canvas.config(scrollregion=(0, 0, self.image_width, self.image_height))
        if self.selection_preview_id is not None:
            self.canvas.tag_raise(self.selection_preview_id)
        if self.preview_item_id is not None:
            self.canvas.tag_raise(self.preview_item_id)

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

    def _mark_modified(self):
        self.is_modified = True
        self._update_window_title()

    def _mark_saved(self):
        self.is_modified = False
        self._update_window_title()

    def _update_window_title(self):
        base_title = "Графічний редактор"
        file_name = "Без назви"
        if self.current_file_path:
            file_name = Path(self.current_file_path).name
        modified_mark = " *" if self.is_modified else ""
        self.root.title(f"{base_title} — {file_name}{modified_mark}")

    def _confirm_discard_changes(self):
        if not self.is_modified:
            return True
        return messagebox.askyesno(
            "Незбережені зміни",
            "Поточне зображення має незбережені зміни. Продовжити без збереження?",
        )

    def _undo(self):
        if not self.undo_stack:
            messagebox.showinfo("Інформація", "Немає дії для скасування.")
            return
        self.image = self.undo_stack.pop()
        self.refresh_canvas()
        self._show_selection_rectangle()
        self._mark_modified()

    def _undo_shortcut(self, event):
        self._undo()

    def _new_image_shortcut(self, event):
        self._new_image()
        return "break"

    def _open_image_shortcut(self, event):
        self._open_image()
        return "break"

    def _save_image_shortcut(self, event):
        self._save_image()
        return "break"

    def _on_mouse_down(self, event):
        x, y = self._get_canvas_coordinates(event)
        self.start_x, self.start_y = x, y
        self.last_x, self.last_y = x, y
        self.is_drawing = True

        if self.current_tool.get() == "Олівець":
            self._save_state_for_undo()

        if self.current_tool.get() == "Виокремити":
            self._clear_selection_preview()

    def _on_mouse_move(self, event):
        if not self.is_drawing:
            return

        x, y = self._get_canvas_coordinates(event)
        tool = self.current_tool.get()

        if tool == "Олівець":
            draw = ImageDraw.Draw(self.image)
            draw.line((self.last_x, self.last_y, x, y), fill=self.line_color, width=self.line_width.get())
            self.last_x, self.last_y = x, y
            self.refresh_canvas()
            return

        if tool == "Виокремити":
            self._update_selection_preview(x, y)
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
            self.refresh_canvas()
            self._mark_modified()
            return

        if tool == "Виокремити":
            self._finalize_selection(x, y)
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
        self._clear_selection()
        self.refresh_canvas()
        self._mark_modified()

    def _cancel_preview(self, event=None):
        self.is_drawing = False
        if self.preview_item_id is not None:
            self.canvas.delete(self.preview_item_id)
            self.preview_item_id = None
        if self.current_tool.get() == "Виокремити":
            self._clear_selection_preview()


    def _clear_selection_preview(self):
        if self.selection_preview_id is not None:
            self.canvas.delete(self.selection_preview_id)
            self.selection_preview_id = None

    def _show_selection_rectangle(self):
        if not self.selection_rect:
            return
        self._clear_selection_preview()
        x1, y1, x2, y2 = self.selection_rect
        self.selection_preview_id = self.canvas.create_rectangle(
            x1, y1, x2, y2, outline="#1e90ff", width=2, dash=(4, 2)
        )

    def _update_selection_preview(self, x, y):
        self._clear_selection_preview()
        self.selection_preview_id = self.canvas.create_rectangle(
            self.start_x, self.start_y, x, y, outline="#1e90ff", width=2, dash=(4, 2)
        )

    def _finalize_selection(self, x, y):
        self.is_drawing = False
        x1, x2 = sorted((self.start_x, x))
        y1, y2 = sorted((self.start_y, y))
        if x1 == x2 or y1 == y2:
            self.selection_rect = None
            self._clear_selection_preview()
            self.status_label.config(text="Виділення скасовано.")
            return
        self.selection_rect = (x1, y1, x2, y2)
        self._show_selection_rectangle()
        self.status_label.config(text="Область виокремлено.")

    def _clear_selection(self):
        self.selection_rect = None
        self._clear_selection_preview()

    def _copy_selection(self):
        if not self.selection_rect:
            messagebox.showinfo("Інформація", "Спочатку виберіть область зображення.")
            return
        x1, y1, x2, y2 = self.selection_rect
        self.copied_fragment = self.image.crop((x1, y1, x2, y2))
        self.status_label.config(text="Виділену область скопійовано.")

    def _paste_selection(self):
        if self.copied_fragment is None:
            messagebox.showinfo("Інформація", "Немає скопійованого фрагмента.")
            return
        self._save_state_for_undo()
        if self.selection_rect:
            paste_x, paste_y = self.selection_rect[0], self.selection_rect[1]
        else:
            paste_x = int(self.canvas.canvasx(0))
            paste_y = int(self.canvas.canvasy(0))
        self.image.paste(self.copied_fragment, (paste_x, paste_y))
        self.refresh_canvas()
        self._show_selection_rectangle()
        self._mark_modified()
        self.status_label.config(text="Скопійований фрагмент вставлено.")

    def _clear_selected_area(self):
        if not self.selection_rect:
            messagebox.showinfo("Інформація", "Спочатку виберіть область зображення.")
            return
        confirmed = messagebox.askyesno("Підтвердження", "Очистити виділену область?")
        if not confirmed:
            return
        self._save_state_for_undo()
        draw = ImageDraw.Draw(self.image)
        draw.rectangle(self.selection_rect, fill="white")
        self.refresh_canvas()
        self._show_selection_rectangle()
        self._mark_modified()
        self.status_label.config(text="Виділену область очищено.")
    def _new_image(self):
        if not self._confirm_discard_changes():
            return
        self._create_new_blank_image(self.image_width, self.image_height)

    def _new_image_with_size(self):
        if not self._confirm_discard_changes():
            return
        width = simpledialog.askinteger(
            "Нове зображення",
            "Введіть ширину (пікселі):",
            initialvalue=800,
            minvalue=1,
        )
        if width is None:
            return
        height = simpledialog.askinteger(
            "Нове зображення",
            "Введіть висоту (пікселі):",
            initialvalue=600,
            minvalue=1,
        )
        if height is None:
            return
        if width <= 0 or height <= 0:
            messagebox.showerror("Помилка", "Ширина і висота мають бути додатними числами.")
            return
        self._create_new_blank_image(width, height)

    def _create_new_blank_image(self, width: int, height: int):
        self.image_width, self.image_height = width, height
        self.image = Image.new("RGB", (width, height), "white")
        self.current_file_path = None
        self.undo_stack.clear()
        self._cancel_preview()
        self._clear_selection()
        self.copied_fragment = None
        self.refresh_canvas()
        self._mark_saved()

    def _open_image(self):
        if not self._confirm_discard_changes():
            return
        file_path = filedialog.askopenfilename(
            title="Відкрити зображення",
            filetypes=[
                ("Зображення", "*.png *.jpg *.jpeg *.bmp"),
                ("PNG", "*.png"),
                ("JPEG", "*.jpg *.jpeg"),
                ("BMP", "*.bmp"),
                ("Усі файли", "*.*"),
            ],
        )
        if not file_path:
            return
        try:
            opened = Image.open(file_path).convert("RGB")
            self.image = opened
            self.image_width, self.image_height = self.image.size
            self.current_file_path = file_path
            self.undo_stack.clear()
            self._cancel_preview()
            self._clear_selection()
            self.copied_fragment = None
            self.refresh_canvas()
            self._mark_saved()
        except Exception:
            messagebox.showerror("Помилка", "Файл не вдалося відкрити.")

    def _save_image(self):
        if not self.current_file_path:
            self._save_image_as()
            return
        try:
            self.image.save(self.current_file_path)
            self._mark_saved()
        except Exception:
            messagebox.showerror("Помилка", "Файл не вдалося зберегти.")

    def _save_image_as(self):
        file_path = filedialog.asksaveasfilename(
            title="Зберегти зображення як",
            defaultextension=".png",
            filetypes=[
                ("PNG", "*.png"),
                ("JPEG", "*.jpg *.jpeg"),
                ("BMP", "*.bmp"),
                ("Усі файли", "*.*"),
            ],
        )
        if not file_path:
            return
        try:
            self.image.save(file_path)
            self.current_file_path = file_path
            self._mark_saved()
        except Exception:
            messagebox.showerror("Помилка", "Файл не вдалося зберегти.")

    def _clear_canvas(self):
        confirmed = messagebox.askyesno(
            "Підтвердження",
            "Очистити полотно? Цю дію можна скасувати через 'Скасувати'.",
        )
        if not confirmed:
            return
        self._save_state_for_undo()
        self.image = Image.new("RGB", (self.image_width, self.image_height), "white")
        self._cancel_preview()
        self._clear_selection()
        self.refresh_canvas()
        self._mark_modified()

    def _exit_app(self):
        if not self._confirm_discard_changes():
            return
        self.root.destroy()

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

    def _apply_image_operation(self, operation_func, status_text: str, clear_selection: bool = False):
        try:
            self._save_state_for_undo()
            new_image = operation_func(self.image)
            self.image = new_image.convert("RGB")
            if clear_selection:
                self._clear_selection()
            self.refresh_canvas()
            self._mark_modified()
            self.status_label.config(text=status_text)
        except Exception:
            messagebox.showerror("Помилка", "Не вдалося виконати операцію із зображенням.")

    def _apply_grayscale(self):
        self._apply_image_operation(
            lambda img: ImageOps.grayscale(img),
            "Застосовано фільтр «Відтінки сірого».",
        )

    def _apply_invert(self):
        self._apply_image_operation(
            lambda img: ImageOps.invert(img),
            "Застосовано «Інверсія кольорів».",
        )

    def _rotate_clockwise(self):
        self._apply_image_operation(
            lambda img: img.transpose(Image.Transpose.ROTATE_270),
            "Зображення повернуто на 90° за годинниковою стрілкою.",
            clear_selection=True,
        )

    def _rotate_counterclockwise(self):
        self._apply_image_operation(
            lambda img: img.transpose(Image.Transpose.ROTATE_90),
            "Зображення повернуто на 90° проти годинникової стрілки.",
            clear_selection=True,
        )

    def _mirror_horizontal(self):
        self._apply_image_operation(
            lambda img: ImageOps.mirror(img),
            "Зображення віддзеркалено горизонтально.",
            clear_selection=True,
        )

    def _mirror_vertical(self):
        self._apply_image_operation(
            lambda img: ImageOps.flip(img),
            "Зображення віддзеркалено вертикально.",
            clear_selection=True,
        )

    def _apply_blur(self):
        self._apply_image_operation(
            lambda img: img.filter(ImageFilter.BLUR),
            "Застосовано розмиття.",
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphicEditorApp(root)
    root.mainloop()
