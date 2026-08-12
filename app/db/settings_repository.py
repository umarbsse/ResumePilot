from dataclasses import dataclass
from typing import Dict

from app.db.database import Database


@dataclass(frozen=True)
class AppSettings:
    ai_prompt: str = ""
    cover_letter_prompt: str = ""
    latex_resume_international: str = ""
    latex_resume_local: str = ""
    cover_letter_resume_international: str = ""
    cover_letter_resume_local: str = ""


class SettingsRepository:
    AI_PROMPT = "ai_prompt"
    COVER_LETTER_PROMPT = "cover_letter_prompt"
    LATEX_RESUME_INTERNATIONAL = "latex_resume_international"
    LATEX_RESUME_LOCAL = "latex_resume_local"
    COVER_LETTER_RESUME_INTERNATIONAL = "cover_letter_resume_international"
    COVER_LETTER_RESUME_LOCAL = "cover_letter_resume_local"

    def __init__(self, database: Database) -> None:
        self.database = database

    def load(self) -> AppSettings:
        values: Dict[str, str] = {}
        with self.database.connection() as connection:
            rows = connection.execute("SELECT key, value FROM settings").fetchall()
            for row in rows:
                values[row["key"]] = row["value"]

        return AppSettings(
            ai_prompt=values.get(self.AI_PROMPT, ""),
            cover_letter_prompt=values.get(self.COVER_LETTER_PROMPT, ""),
            latex_resume_international=values.get(self.LATEX_RESUME_INTERNATIONAL, ""),
            latex_resume_local=values.get(self.LATEX_RESUME_LOCAL, ""),
            cover_letter_resume_international=values.get(
                self.COVER_LETTER_RESUME_INTERNATIONAL, ""
            ),
            cover_letter_resume_local=values.get(self.COVER_LETTER_RESUME_LOCAL, ""),
        )

    def save(self, settings: AppSettings) -> None:
        items = {
            self.AI_PROMPT: settings.ai_prompt,
            self.COVER_LETTER_PROMPT: settings.cover_letter_prompt,
            self.LATEX_RESUME_INTERNATIONAL: settings.latex_resume_international,
            self.LATEX_RESUME_LOCAL: settings.latex_resume_local,
            self.COVER_LETTER_RESUME_INTERNATIONAL: settings.cover_letter_resume_international,
            self.COVER_LETTER_RESUME_LOCAL: settings.cover_letter_resume_local,
        }

        with self.database.connection() as connection:
            connection.executemany(
                """
                INSERT INTO settings (key, value, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(key) DO UPDATE SET
                    value = excluded.value,
                    updated_at = CURRENT_TIMESTAMP
                """,
                items.items(),
            )
