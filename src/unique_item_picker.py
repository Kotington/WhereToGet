import tkinter as tk
from tkinter import font
import sys
import os
import json

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    return os.path.normpath(os.path.join(base_path, relative_path))

def parse_items(language="en"):
    file_name = "WhereToGet/data/items_en.json" if language == "en" else "WhereToGet/data/items_ru.json"
    file_path = resource_path(file_name)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            items = json.load(f)
    except FileNotFoundError:
        print(f"[Ошибка] Файл не найден: {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"[Ошибка] Некорректный JSON: {file_path}")
        return []

    # Добавляем ID для каждого предмета, если его нет
    for idx, item in enumerate(items):
        item["id"] = idx

    return items

class UniquePickerApp:
    def __init__(self, root):
        self.root = root
        self.translations = {
            "en": {
                "title": "WhereToGet",
                "left_label": "Unique Items",
                "right_label": "Selected Items",
                "search_placeholder": ""
            },
            "ru": {
                "title": "WhereToGet",
                "left_label": "Уникальные предметы",
                "right_label": "Выбранные предметы",
                "search_placeholder": ""
            }
        }

        self.language = self.load_language()
        self.items = parse_items(self.language)
        self.filtered_items = self.items.copy()
        self.selected_items = []
        self.load_selected_items()

        self.root.title(self.translations[self.language]["title"])
        self.root.geometry("950x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#121212")

        self.font_normal = font.Font(family="Helvetica", size=10)
        self.font_bold = font.Font(family="Helvetica", size=10, weight="bold")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # === МЕНЮ ВЫБОРА ЯЗЫКА ===
        self.lang_frame = tk.Frame(self.root, bg="#2a2a2a", height=40)
        self.lang_frame.pack(side="top", fill="x")

        self.lang_var = tk.StringVar(value="English" if self.language == "en" else "Русский")
        self.lang_menu = tk.OptionMenu(
            self.lang_frame,
            self.lang_var,
            "English",
            "Русский",
            command=self.change_language
        )
        self.lang_menu.config(bg="#1e1e1e", fg="white", bd=0, highlightthickness=0, font=self.font_normal)
        self.lang_menu["menu"].config(bg="#1e1e1e", fg="white", font=self.font_normal)
        self.lang_menu.pack(side="left", padx=10, pady=5)

        # === ЛЕВАЯ КОЛОНКА С ПОИСКОМ И СПИСКОМ ===
        self.left_frame = tk.Frame(self.root, bg="#2a2a2a", width=170)
        self.left_frame.pack(side="left", fill="y")

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            self.left_frame,
            textvariable=self.search_var,
            font=self.font_normal,
            fg="white",
            bg="#1e1e1e",
            insertbackground="white"
        )
        self.search_entry.pack(padx=10, pady=10, fill="x")
        self.search_entry.insert(0, self.translations[self.language]["search_placeholder"])

        def clear_placeholder_and_reset_scroll():
            if self.search_var.get().lower() == self.translations[self.language]["search_placeholder"].lower():
                self.search_entry.delete(0, tk.END)
            self.filter_list()
            self.left_canvas.yview_moveto(0)  # Сброс прокрутки

        self.search_entry.bind("<KeyRelease>", lambda e: clear_placeholder_and_reset_scroll())
        self.search_entry.bind("<FocusIn>", lambda e: self.clear_placeholder())
        self.search_entry.bind("<FocusOut>", lambda e: restore_placeholder())

        def clear_placeholder():
            if self.search_var.get().lower() == self.translations[self.language]["search_placeholder"].lower():
                self.search_entry.delete(0, tk.END)

        def restore_placeholder():
            if not self.search_var.get():
                self.search_entry.delete(0, tk.END)
                self.search_entry.insert(0, self.translations[self.language]["search_placeholder"])

        self.left_label = tk.Label(
            self.left_frame, text=self.translations[self.language]["left_label"],
            bg="#2a2a2a", fg="white", font=self.font_bold
        )
        self.left_label.pack(pady=5)

        self.left_canvas = tk.Canvas(self.left_frame, bg="#2a2a2a", highlightthickness=0)
        self.left_container = tk.Frame(self.left_canvas, bg="#2a2a2a", highlightthickness=0)
        self.left_container.bind("<Configure>",
                                 lambda e: self.left_canvas.configure(scrollregion=self.left_canvas.bbox("all")))
        self.left_canvas.create_window((0, 0), window=self.left_container, anchor="nw")

        # === КАСТОМНЫЙ СКРОЛЛБАР (левый) ===
        self.custom_scrollbar_left = tk.Frame(self.left_frame, width=8, bg="#1e1e1e")
        self.custom_scrollbar_left.pack_propagate(False)
        self.custom_scrollbar_left.pack(side="right", fill="y")
        self.scroll_thumb_left = tk.Frame(self.custom_scrollbar_left, bg="#3a3a3a", width=8)
        self.scroll_thumb_left.pack(fill="y", expand=True)

        self.left_canvas.pack(side="left", fill="both", expand=True)
        self._add_hover_bind(self.left_canvas, self.left_canvas)
        self._add_hover_bind(self.left_container, self.left_canvas)

        self.item_buttons = []
        self.update_left_list(self.items)

        # === ПРАВАЯ КОЛОНКА С ВЫБРАННЫМИ ПРЕДМЕТАМИ ===
        self.right_frame = tk.Frame(self.root, bg="#121212")
        self.right_frame.pack(fill="both", expand=True, padx=(0, 10))

        self.right_label = tk.Label(
            self.right_frame, text=self.translations[self.language]["right_label"],
            bg="#121212", fg="white", font=self.font_bold
        )
        self.right_label.pack(pady=10)

        self.right_canvas = tk.Canvas(self.right_frame, bg="#121212", highlightthickness=0)
        self.right_container = tk.Frame(self.right_canvas, bg="#121212", highlightthickness=0)
        self.right_container.bind("<Configure>",
                                  lambda e: self.right_canvas.configure(scrollregion=self.right_canvas.bbox("all")))
        self.right_canvas.create_window((0, 0), window=self.right_container, anchor="nw")

        # === КАСТОМНЫЙ СКРОЛЛБАР (правый) ===
        self.custom_scrollbar_right = tk.Frame(self.right_frame, width=8, bg="#1e1e1e")
        self.custom_scrollbar_right.pack_propagate(False)
        self.custom_scrollbar_right.pack(side="right", fill="y", pady=(10, 0))
        self.scroll_thumb_right = tk.Frame(self.custom_scrollbar_right, bg="#3a3a3a", width=8)
        self.scroll_thumb_right.pack(fill="y", expand=True)

        self.right_canvas.pack(side="left", fill="both", expand=True, pady=(10, 0))
        self._add_hover_bind(self.right_canvas, self.right_canvas)
        self._add_hover_bind(self.right_container, self.right_canvas)

        self.update_right_panel()

        # Привязка событий кастомной прокрутки
        self.root.bind_all("<MouseWheel>", lambda e: self.on_custom_scroll(e, self.left_canvas, self.scroll_thumb_left))
        self.root.bind_all("<MouseWheel>", lambda e: self.on_custom_scroll(e, self.right_canvas, self.scroll_thumb_right))
        self.scroll_thumb_left.bind("<ButtonPress-1>", lambda e: self.on_drag_start(e, self.left_canvas, self.scroll_thumb_left))
        self.scroll_thumb_left.bind("<B1-Motion>", lambda e: self.on_drag_motion(e, self.left_canvas, self.scroll_thumb_left))
        self.scroll_thumb_right.bind("<ButtonPress-1>", lambda e: self.on_drag_start(e, self.right_canvas, self.scroll_thumb_right))
        self.scroll_thumb_right.bind("<B1-Motion>", lambda e: self.on_drag_motion(e, self.right_canvas, self.scroll_thumb_right))

    def _on_mousewheel(self, event, canvas):
        try:
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except tk.TclError:
            pass

    def _bind_mousewheel(self, canvas):
        self.root.bind_all("<MouseWheel>", lambda e: self._on_mousewheel(e, canvas))

    def _unbind_mousewheel(self):
        self.root.unbind_all("<MouseWheel>")

    def _add_hover_bind(self, widget, canvas):
        widget.bind("<Enter>", lambda e: self._bind_mousewheel(canvas))
        widget.bind("<Leave>", lambda e: self._unbind_mousewheel())

    def update_left_list(self, items):
        for btn in self.item_buttons:
            btn.destroy()
        self.item_buttons.clear()
        for item in items:
            btn = tk.Label(
                self.left_container,
                text=item["name"],
                bg="#2a2a2a",
                fg="orange",
                font=self.font_normal,
                cursor="hand2"
            )
            btn.pack(anchor="w", padx=10, pady=2)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#3a3a3a"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#2a2a2a"))
            btn.bind("<Button-1>", lambda e, i=item: self.add_to_selected(i))
            self._add_hover_bind(btn, self.left_canvas)
            self.item_buttons.append(btn)

    def filter_list(self):
        query = self.search_var.get().lower()
        placeholder = self.translations[self.language]["search_placeholder"].lower()
        if query == placeholder:
            query = ""
        self.filtered_items = [
            item for item in self.items
            if query in item["name"].lower()
        ]
        self.update_left_list(self.filtered_items)
        self.root.after_idle(lambda: self._update_custom_scrollbar(self.left_canvas, self.scroll_thumb_left))

    def add_to_selected(self, item):
        if item not in self.selected_items:
            self.selected_items.append(item)
            self.update_right_panel()

    def remove_from_selected(self, item):
        if item in self.selected_items:
            self.selected_items.remove(item)
            self.update_right_panel()

    def update_right_panel(self):
        for widget in self.right_container.winfo_children():
            widget.destroy()

        for item in self.selected_items:
            card_frame = tk.Frame(
                self.right_container,
                bg="#2c2c2c",
                bd=1,
                relief="solid",
                highlightthickness=0
            )
            card_frame.pack(padx=10, pady=5, fill="x")

            content_frame = tk.Frame(card_frame, bg="#2c2c2c", highlightthickness=0)
            content_frame.pack(padx=10, pady=10, fill="x")

            wraplength_px = 510 - 2 * 10

            title = tk.Label(
                content_frame,
                text=item["name"],
                bg="#2c2c2c",
                fg="white",
                font=self.font_bold,
                anchor="w",
                wraplength=wraplength_px,
                justify="left",
                highlightthickness=0
            )
            title.pack(anchor="w")

            type_label = tk.Label(
                content_frame,
                text=f"Type: {item['type']}" if self.language == "en" else f"Тип: {item['type']}",
                bg="#2c2c2c",
                fg="lightgray",
                anchor="w",
                wraplength=wraplength_px,
                justify="left",
                highlightthickness=0
            )
            type_label.pack(anchor="w", pady=(1, 0))

            unique_name = item.get("subtype", "")
            if unique_name:
                unique_name_label = tk.Label(
                    content_frame,
                    text=unique_name,
                    bg="#2c2c2c",
                    fg="lightgray",
                    anchor="w",
                    wraplength=wraplength_px,
                    justify="left",
                    highlightthickness=0
                )
                unique_name_label.pack(anchor="w", pady=(1, 0))
            else:
                unique_name_label = None

            obtained_lines = item.get("obtained", [])
            label_list = []
            for line in obtained_lines:
                label = tk.Label(
                    content_frame,
                    text="• " + line,
                    bg="#2c2c2c",
                    fg="lightgray",
                    anchor="w",
                    wraplength=wraplength_px,
                    justify="left",
                    highlightthickness=0
                )
                label.pack(anchor="w", padx=5, pady=(1, 0))
                label_list.append(label)

            clickables = [card_frame, content_frame, title, type_label]
            if unique_name_label:
                clickables.append(unique_name_label)
            clickables.extend(label_list)

            for widget in clickables:
                widget.bind("<Button-1>", lambda e, i=item: self.remove_from_selected(i))
                self._add_hover_bind(widget, self.right_canvas)

        self.right_container.update_idletasks()
        self.root.after_idle(lambda: self._update_custom_scrollbar(self.right_canvas, self.scroll_thumb_right))

    def _update_custom_scrollbar(self, canvas, scroll_thumb):
        bbox = canvas.bbox("all")
        canvas_height = canvas.winfo_height()
        if not bbox or canvas_height <= 0 or bbox[3] <= 0:
            scroll_thumb.place_forget()
            return
        if bbox[3] <= canvas_height:
            scroll_thumb.place_forget()
            return
        relheight = max(0.05, canvas_height / bbox[3])
        yview = canvas.yview()
        scroll_thumb.place(relheight=relheight, width=8, x=0, rely=yview[0])

    def on_custom_scroll(self, event, canvas, scroll_thumb):
        try:
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            self.root.after_idle(lambda: self._update_custom_scrollbar(canvas, scroll_thumb))
        except tk.TclError:
            pass

    def on_drag_start(self, e, canvas, scroll_thumb):
        e.widget.start_y = e.y

    def on_drag_motion(self, e, canvas, scroll_thumb):
        dy = e.y - e.widget.start_y
        total_size = canvas.bbox("all")[3]
        visible_size = canvas.winfo_height()
        if total_size > visible_size:
            delta = dy / (total_size - visible_size) * total_size
            canvas.yview_scroll(int(delta), "units")
            self.root.after_idle(lambda: self._update_custom_scrollbar(canvas, scroll_thumb))
        e.widget.start_y = e.y

    def save_selected_items(self):
        file_path = resource_path("selected_items.json")
        selected_ids = [item["id"] for item in self.selected_items]
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(selected_ids, f)

    def load_selected_items(self):
        file_path = resource_path("selected_items.json")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                selected_ids = set(json.load(f))
            id_to_item = {item["id"]: item for item in self.items}
            self.selected_items = [id_to_item[_id] for _id in selected_ids if _id in id_to_item]
        except (FileNotFoundError, json.JSONDecodeError):
            self.selected_items = []

    def save_language(self):
        file_path = resource_path("settings.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump({"language": self.language}, f)

    def load_language(self):
        file_path = resource_path("settings.json")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                settings = json.load(f)
            return settings.get("language", "en")
        except (FileNotFoundError, json.JSONDecodeError):
            return "en"

    def change_language(self, choice):
        self.language = "en" if choice == "English" else "ru"
        self.save_language()
        self.root.title(self.translations[self.language]["title"])
        self.left_label.config(text=self.translations[self.language]["left_label"])
        self.right_label.config(text=self.translations[self.language]["right_label"])
        self.search_entry.delete(0, tk.END)
        self.search_entry.insert(0, self.translations[self.language]["search_placeholder"])
        new_items = parse_items(self.language)
        selected_ids = {item["id"] for item in self.selected_items}
        id_to_item = {item["id"]: item for item in new_items}
        self.selected_items = [id_to_item[_id] for _id in selected_ids if _id in id_to_item]
        self.items = new_items
        self.filter_list()
        self.update_right_panel()
        self.root.bind_all("<MouseWheel>", lambda e: self.on_custom_scroll(e, self.left_canvas, self.scroll_thumb_left))
        self.root.bind_all("<MouseWheel>", lambda e: self.on_custom_scroll(e, self.right_canvas, self.scroll_thumb_right))

    def on_close(self):
        self.save_selected_items()
        self.save_language()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = UniquePickerApp(root)
    root.mainloop()