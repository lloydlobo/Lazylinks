import json
import os.path
import subprocess
import tkinter as tk
import webbrowser
from tkinter import filedialog, messagebox, ttk

CONFIG_JSON = "config.json"
VERSION = "v0.01"


class ConfigManager:
    @staticmethod
    def load_config(file_path):
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Configuration file not found: {file_path}.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON in configuration file: {file_path}.")
        return None

    @staticmethod
    def save_config(file_path, config):
        try:
            with open(file_path, "w") as config_file:
                json.dump(config, config_file)
            print(f"Configuration exported to: {file_path}")
        except OSError as err:
            print(f"Error saving configuration: {err}")


class CmdEvent:
    @staticmethod
    def exit_window(root):
        root.destroy()

    @staticmethod
    def reload_window(root):
        root.destroy()
        main()

    @staticmethod
    def click_link(event, link):
        webbrowser.open(link)

    @staticmethod
    def click_link_batch(event, links):
        for link in links:
            CmdEvent.click_link(event=event, link=link)

    @staticmethod
    def open_selected_listbox_link(event, listbox):
        webbrowser.open(selected_link := listbox.get(tk.ANCHOR))

    @staticmethod
    def open_active_listbox_link(event, listbox):
        webbrowser.open(active_link := listbox.get(tk.ACTIVE))

    @staticmethod
    def export_config():
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Export Config",
        )

        if file_path:
            ConfigManager.save_config(file_path, config)

    @staticmethod
    def import_config():
        file_path = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Import Config",
        )

        if file_path:
            ConfigManager.load_config(file_path)
        return None

    @staticmethod
    def edit_config():
        file_path = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Edit Config",
        )

        if file_path:
            try:
                assert os.path.basename(file_path) == CONFIG_JSON, f"Selected file '{file_path}' is not '{CONFIG_JSON}'"
            except AssertionError as assertion_err:
                messagebox.showerror("Error", f"Invalid file selected: {assertion_err}")
                return
            try:
                subprocess.Popen([file_path], shell=True)
            except Exception as err:
                print(f"Error opening file: {err}")


class App:
    @staticmethod
    def setup_main_window(root, config):
        general_config = config["general"]
        colors_config = config["colors"]
        fonts_config = config["fonts"]
        typography_config = config["typography"]
        links_config = config["links"]

        ttk.Style().configure("TButton", padding=5, relief="flat", background="#ccc")

        menu_bar = tk.Menu(root)
        root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu = tk.Menu(menu_bar, tearoff=0)

        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Edit Config", command=CmdEvent.edit_config)
        file_menu.add_command(label="Reload Window", command=lambda: CmdEvent.reload_window(root))
        file_menu.add_command(label="Exit", command=lambda: CmdEvent.exit_window(root))

        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=lambda: messagebox.showinfo(
            title="Lazylinks",
            message=f"Lazily opens links\n\n{'Version: '}{VERSION}\n{'Configuration: '}{CONFIG_JSON}\n"
        ))

        frame_head = tk.Frame(root, padx=5, pady=5, bg=colors_config["bg_primary"])
        label_links = tk.Label(
            frame_head, text=general_config["title"],
            font=(fonts_config["font_mono"], typography_config["text_base"]),
            background=colors_config["bg_primary"], foreground=colors_config["fg_primary"], pady=0, padx=0,
        )
        btn_open_all_links = tk.Button(
            frame_head, text="Open All",
            font=(fonts_config["font_mono"], typography_config["text_base"], None or "bold"),
            bg=colors_config["bg_secondary"], fg=colors_config["bg_accent"],
            activebackground=colors_config["bg_secondary"], activeforeground=colors_config["fg_accent"],
            padx=5, pady=0, relief=tk.FLAT,
            command=lambda: CmdEvent.click_link_batch(None, links_config),
        )
        listbox_links = tk.Listbox(
            root, font=(fonts_config["font_mono"], typography_config["text_base"]),
            background=colors_config["bg_secondary"], foreground=colors_config["fg_primary"],
            selectbackground=colors_config["bg_primary"], selectforeground=colors_config["fg_primary"],
            height=5, highlightthickness=1, highlightbackground=colors_config["bg_primary"],
            highlightcolor=colors_config["bg_accent"], relief=tk.FLAT, borderwidth=5,
        )

        root.title(general_config["title"])
        root.configure(bg=colors_config["bg_primary"], padx=0)

        for link in links_config:
            listbox_links.insert(tk.END, link)

        listbox_links.bind("<Double-Button-1>", lambda event: CmdEvent.open_selected_listbox_link(event, listbox_links))
        listbox_links.bind("<Return>", lambda event: CmdEvent.open_active_listbox_link(event, listbox_links))

        frame_head.pack(fill=tk.BOTH)
        label_links.pack(side=tk.LEFT)
        btn_open_all_links.pack(side=tk.RIGHT, padx=2, pady=0)
        listbox_links.pack(expand=True, fill=tk.BOTH)


def main():
    config = ConfigManager.load_config(file_path=CONFIG_JSON)

    if config is not None:
        root = tk.Tk()
        window_config = config.get("general", {}).get("window", {})
        root.geometry(f'{window_config.get("width", 300)}x{window_config.get("height", 500)}')
        App.setup_main_window(root=root, config=config)
        root.mainloop()


if __name__ == '__main__':
    main()
