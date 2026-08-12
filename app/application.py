from app.config import DATABASE_PATH
from app.db.database import Database
from app.db.settings_repository import SettingsRepository
from app.services.job_processor import JobProcessor
from app.ui.main_window import MainWindow


class JobApplyApplication:
    def __init__(self) -> None:
        database = Database(DATABASE_PATH)
        repository = SettingsRepository(database)
        processor = JobProcessor()
        self.window = MainWindow(repository, processor)

    def run(self) -> None:
        self.window.mainloop()
