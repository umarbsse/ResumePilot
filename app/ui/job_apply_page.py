import tkinter as tk
from tkinter import messagebox, ttk

from app.db.settings_repository import AppSettings, SettingsRepository
from app.services.job_processor import JobProcessor
from app.ui.widgets import LabeledText


class JobApplyPage(ttk.Frame):
    LOCAL = "Local"
    INTERNATIONAL = "International"

    def __init__(
        self,
        parent: tk.Misc,
        repository: SettingsRepository,
        processor: JobProcessor,
    ) -> None:
        super().__init__(parent, padding=20)
        self.repository = repository
        self.processor = processor
        self.settings = AppSettings()
        self.resume_type = tk.StringVar(value=self.INTERNATIONAL)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        header = ttk.Frame(self)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 4))
        header.columnconfigure(0, weight=1)
        ttk.Label(header, text="Job Apply", style="Title.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Button(header, text="+ Add New Job", command=self.new_job, style="Primary.TButton").grid(
            row=0, column=1, sticky="e"
        )

        ttk.Label(
            self,
            text="Load your saved prompt and resume, add a job description, then build the final AI input.",
        ).grid(row=1, column=0, sticky="w", pady=(0, 16))

        content = ttk.Frame(self)
        content.grid(row=2, column=0, sticky="nsew")
        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=1)
        content.rowconfigure(0, weight=1)
        content.rowconfigure(1, weight=2)

        self.ai_prompt = LabeledText(content, "AI Prompt (loaded from Settings)", height=8)
        self.job_description = LabeledText(content, "Job Description", height=8)
        self.output = LabeledText(content, "Processed Output", height=20, wrap="none")

        self.ai_prompt.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=(0, 12))
        self.job_description.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=(0, 12))

        resume_panel = ttk.Frame(content)
        resume_panel.grid(row=1, column=0, sticky="nsew", padx=(0, 8))
        resume_panel.columnconfigure(0, weight=1)
        resume_panel.rowconfigure(1, weight=1)

        self.resume = LabeledText(resume_panel, "User LaTeX Resume Code", height=20, wrap="none")

        selector = ttk.Frame(resume_panel)
        selector.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        ttk.Label(selector, text="Resume Type:").pack(side="left")
        ttk.Radiobutton(
            selector,
            text=self.INTERNATIONAL,
            value=self.INTERNATIONAL,
            variable=self.resume_type,
            command=self._load_selected_resume,
        ).pack(side="left", padx=(10, 6))
        ttk.Radiobutton(
            selector,
            text=self.LOCAL,
            value=self.LOCAL,
            variable=self.resume_type,
            command=self._load_selected_resume,
        ).pack(side="left", padx=6)
        self.resume.grid(row=1, column=0, sticky="nsew")

        self.output.grid(row=1, column=1, sticky="nsew", padx=(8, 0))

        footer = ttk.Frame(self)
        footer.grid(row=3, column=0, sticky="ew", pady=(16, 0))
        footer.columnconfigure(0, weight=1)
        ttk.Button(footer, text="Copy Output", command=self.copy_output).grid(row=0, column=1, padx=(0, 8))
        ttk.Button(footer, text="Process", command=self.process, style="Primary.TButton").grid(row=0, column=2)

        self.new_job()

    def new_job(self) -> None:
        self.settings = self.repository.load()
        self.ai_prompt.set(self.settings.ai_prompt)
        self.job_description.set("")
        self.output.set("")
        self._load_selected_resume()

    def _load_selected_resume(self) -> None:
        if self.resume_type.get() == self.LOCAL:
            value = self.settings.latex_resume_local
        else:
            value = self.settings.latex_resume_international
        self.resume.set(value)

    def process(self) -> None:
        ai_prompt = self.ai_prompt.get()
        job_description = self.job_description.get()
        latex_resume = self.resume.get()

        missing = []
        if not ai_prompt.strip():
            missing.append("AI Prompt")
        if not job_description.strip():
            missing.append("Job Description")
        if not latex_resume.strip():
            missing.append("LaTeX Resume Code")

        if missing:
            messagebox.showwarning(
                "Missing fields",
                "Please complete: " + ", ".join(missing),
            )
            return

        final_text = self.processor.build_input(ai_prompt, job_description, latex_resume)
        self.output.set(final_text)

    def copy_output(self) -> None:
        value = self.output.get()
        if not value.strip():
            messagebox.showinfo("Nothing to copy", "Process a job first.")
            return
        self.clipboard_clear()
        self.clipboard_append(value)
        self.update()
        messagebox.showinfo("Copied", "Processed output copied to the clipboard.")
