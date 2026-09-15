import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"


def load_env_file(env_path: Path = ENV_FILE):
    if env_path.is_file() is False:
        return

    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip("'\""))


def validate_config(env_path: Path = ENV_FILE):
    load_env_file(env_path)

    # DB_FILE
    DB_FILE_RAW = os.getenv("DB_FILE")
    if DB_FILE_RAW is None or DB_FILE_RAW.strip() is None:
        return Path(".sdb")

    path = Path(DB_FILE_RAW.strip())
    parent_dir = path.parent

    if parent_dir and str(parent_dir) != ".":
        try:
            parent_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise PermissionError(
                f"Cannot write to directory DB_FILE '{parent_dir}': {e}"
            )

    return path
