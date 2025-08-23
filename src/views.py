import tkinter as tk
from tkinter import ttk, messagebox
from typing import TYPE_CHECKING

from .utils import get_files_in_dir

if TYPE_CHECKING:
    from src.controllers import Controller

SCALE = 3
BOX_SIZE = 10 * SCALE
WIDTH = 10 * BOX_SIZE
HEIGHT = 20 * BOX_SIZE


class BaseView(tk.Frame):
    def __init__(self, parent: tk.Tk, controller: "Controller"):
        super().__init__(parent)
        self.controller = controller


class LoggerView(BaseView):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.label = tk.Label(self, text="Logger UI", font=("Arial", 24))
        self.label.pack(pady=BOX_SIZE // 2)

        self.view_settings_btn = tk.Button(
            self, text="View Settings", command=self.controller.show_settings_view
        )
        self.view_settings_btn.pack()

        self.start_log_pulse_btn = tk.Button(
            self, text="Start Log Pulse", command=self.controller.start_scheduler
        )
        self.start_log_pulse_btn.pack()


class SettingsView(BaseView):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller

        file_options = get_files_in_dir("logs", [".md"])

        self.label = tk.Label(self, text="Settings UI", font=("Arial", 24))
        self.label.pack(pady=20)

        self.log_option_frame = tk.Frame(self)

        self.log_options_var = tk.StringVar()
        self.log_options = ttk.Combobox(
            self.log_option_frame,
            textvariable=self.log_options_var,
            state="readonly",
            values=file_options,
        )

        self.refresh_options_btn = tk.Button(
            self.log_option_frame, text="Refresh", command=self.refresh_file_list
        )

        self.log_options.pack()
        self.log_option_frame.pack()

        self.refresh_btn = tk.Button(
            self, text="Refresh files", command=self.refresh_file_list
        )
        self.refresh_btn.pack(pady=BOX_SIZE // 2)

        self.button = tk.Button(
            self, text="Change Message", command=self.controller.show_logger_view
        )
        self.button.pack(pady=50, padx=100)

    def refresh_file_list(self):
        try:
            file_options = get_files_in_dir("logs", [".md"])

            if file_options:
                self.log_options["values"] = file_options
                selected_option = self.log_options_var.get()
                self.log_options.set(
                    selected_option
                    if selected_option in file_options
                    else file_options[0]
                )
            else:
                self.log_options["values"] = []
                self.log_options.set("")

        except Exception as e:
            # If you're running as .pyw (no console), show errors visibly
            messagebox.showerror("Error", f"Failed to read files:\n{e}")
