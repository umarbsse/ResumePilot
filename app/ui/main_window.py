import tkinter as tk
from tkinter import ttk
from typing import Dict

from app.config import APP_NAME, MIN_WINDOW_HEIGHT, MIN_WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_WIDTH
from app.db.settings_repository import SettingsRepository
from app.services.job_processor import JobProcessor
from app.ui.job_apply_page import JobApplyPage
from app.ui.settings_page import SettingsPage


class MainWindow(tk.Tk):
    def __init__(self, repository: SettingsRepository, processor: JobProcessor) -> None:
        super().__init__()
        self.title(APP_NAME)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)

        self._configure_styles()
        self._build_layout(repository, processor)

    def _configure_styles(self) -> None:
        style = ttk.Style(self)
        if "clam" in style.theme_names():
            style.theme_use("clam")

        style.configure("Title.TLabel", font=("TkDefaultFont", 18, "bold"))
        style.configure("Nav.TButton", padding=(14, 10), anchor="w")
        style.configure("Primary.TButton", padding=(14, 8))

    def _build_layout(self, repository: SettingsRepository, processor: JobProcessor) -> None:
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        sidebar = ttk.Frame(self, padding=12)
        sidebar.grid(row=0, column=0, sticky="nsw")
        ttk.Label(sidebar, text=APP_NAME, font=("TkDefaultFont", 12, "bold")).pack(
            anchor="w", pady=(4, 18)
        )

        container = ttk.Frame(self)
        container.grid(row=0, column=1, sticky="nsew")
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)

        self.pages: Dict[str, ttk.Frame] = {
            "job": JobApplyPage(container, repository, processor),
            "settings": SettingsPage(container, repository),
        }
        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew")

        ttk.Button(sidebar, text="Job Apply", style="Nav.TButton", command=lambda: self.show_page("job")).pack(
            fill="x", pady=3
        )
        ttk.Button(sidebar, text="Settings", style="Nav.TButton", command=lambda: self.show_page("settings")).pack(
            fill="x", pady=3
        )

        self.show_page("job")

    def show_page(self, name: str) -> None:
        page = self.pages[name]
        if name == "job" and isinstance(page, JobApplyPage):
            # Refresh saved values every time the user opens Job Apply.
            page.new_job()
        elif name == "settings" and isinstance(page, SettingsPage):
            page.load_settings()
        page.tkraise()
