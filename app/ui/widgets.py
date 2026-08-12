import tkinter as tk
from tkinter import ttk


class LabeledText(ttk.Frame):
    def __init__(
        self,
        parent: tk.Misc,
        label: str,
        height: int = 8,
        wrap: str = "word",
    ) -> None:
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        ttk.Label(self, text=label).grid(row=0, column=0, sticky="w", pady=(0, 6))
        text_frame = ttk.Frame(self)
        text_frame.grid(row=1, column=0, sticky="nsew")
        text_frame.rowconfigure(0, weight=1)
        text_frame.columnconfigure(0, weight=1)

        self.text = tk.Text(
            text_frame,
            height=height,
            wrap=wrap,
            undo=True,
            padx=10,
            pady=8,
            relief="solid",
            borderwidth=1,
        )
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=scrollbar.set)

        self.text.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

    def get(self) -> str:
        return self.text.get("1.0", "end-1c")

    def set(self, value: str) -> None:
        self.text.delete("1.0", "end")
        self.text.insert("1.0", value or "")
