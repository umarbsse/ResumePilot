from pathlib import Path

APP_NAME = "ResumePilot"
APP_DIR_NAME = ".resumepilot"

USER_DATA_DIR = Path.home() / APP_DIR_NAME
DATABASE_PATH = USER_DATA_DIR / "resumepilot.db"

WINDOW_WIDTH = 1180
WINDOW_HEIGHT = 760
MIN_WINDOW_WIDTH = 960
MIN_WINDOW_HEIGHT = 640
