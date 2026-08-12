import tkinter as tk
from tkinter import messagebox, ttk

from app.db.settings_repository import AppSettings, SettingsRepository
from app.ui.widgets import LabeledText


class SettingsPage(ttk.Frame):
    def __init__(self, parent: tk.Misc, repository: SettingsRepository) -> None:
        super().__init__(parent, padding=20)
        self.repository = repository

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        ttk.Label(self, text="Settings", style="Title.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 4)
        )
        ttk.Label(
            self,
            text="Store prompts and LaTeX resume templates used by ResumePilot.",
        ).grid(row=1, column=0, sticky="w", pady=(0, 16))

        body = ttk.Frame(self)
        body.grid(row=2, column=0, sticky="nsew")
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)
        body.rowconfigure(1, weight=2)
        body.rowconfigure(2, weight=2)

        self.ai_prompt = LabeledText(body, "AI Prompt", height=6)
        self.cover_letter_prompt = LabeledText(body, "Cover Letter Prompt", height=6)
        self.resume_international = LabeledText(
            body, "User LaTeX Resume Code (International)", height=12, wrap="none"
        )
        self.resume_local = LabeledText(
            body, "User LaTeX Resume Code (Local)", height=12, wrap="none"
        )
        self.cover_letter_resume_international = LabeledText(
            body, "Cover letter resume code (International)", height=12, wrap="none"
        )
        self.cover_letter_resume_local = LabeledText(
            body, "Cover letter resume code (Local)", height=12, wrap="none"
        )

        self.ai_prompt.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=(0, 12))
        self.cover_letter_prompt.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=(0, 12))
        self.resume_international.grid(
            row=1, column=0, sticky="nsew", padx=(0, 8), pady=(0, 12)
        )
        self.resume_local.grid(
            row=1, column=1, sticky="nsew", padx=(8, 0), pady=(0, 12)
        )
        self.cover_letter_resume_international.grid(
            row=2, column=0, sticky="nsew", padx=(0, 8)
        )
        self.cover_letter_resume_local.grid(
            row=2, column=1, sticky="nsew", padx=(8, 0)
        )

        footer = ttk.Frame(self)
        footer.grid(row=3, column=0, sticky="ew", pady=(16, 0))
        footer.columnconfigure(0, weight=1)
        ttk.Button(footer, text="Reload", command=self.load_settings).grid(
            row=0, column=1, padx=(0, 8)
        )
        ttk.Button(
            footer,
            text="Save Settings",
            command=self.save_settings,
            style="Primary.TButton",
        ).grid(row=0, column=2)

        self.load_settings()

    def load_settings(self) -> None:
        settings = self.repository.load()
        self.ai_prompt.set(settings.ai_prompt)
        self.cover_letter_prompt.set(settings.cover_letter_prompt)
        self.resume_international.set(settings.latex_resume_international)
        self.resume_local.set(settings.latex_resume_local)
        self.cover_letter_resume_international.set(
            settings.cover_letter_resume_international
        )
        self.cover_letter_resume_local.set(settings.cover_letter_resume_local)

    def save_settings(self) -> None:
        settings = AppSettings(
            ai_prompt=self.ai_prompt.get(),
            cover_letter_prompt=self.cover_letter_prompt.get(),
            latex_resume_international=self.resume_international.get(),
            latex_resume_local=self.resume_local.get(),
            cover_letter_resume_international=self.cover_letter_resume_international.get(),
            cover_letter_resume_local=self.cover_letter_resume_local.get(),
        )
        self.repository.save(settings)
        messagebox.showinfo("Saved", "Settings were saved successfully.")
