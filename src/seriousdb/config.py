import os
from pathlib import Path
from dataclasses import dataclass

BASE_DIR = Path(__file__).cwd()
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


@dataclass(frozen=True)
class Config:
    db_file: Path

    @classmethod
    def load(cls, env_path: Path = ENV_FILE) -> "Config":
        load_env_file(env_path)

        # DB_FILE
        DB_FILE_RAW = os.getenv("DB_FILE", ".sdb")

        path = Path(DB_FILE_RAW.strip())
        parent_dir = path.parent

        if parent_dir and str(parent_dir) != ".":
            try:
                parent_dir.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                raise PermissionError(
                    f"Cannot write to directory DB_FILE '{parent_dir}': {e}"
                )

        return cls(db_file=path)


config = Config.load()
