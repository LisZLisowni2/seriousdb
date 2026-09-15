import os
import shutil
import tempfile
import unittest
from pathlib import Path

from seriousdb.config import Config, load_env_file


class ConfigurationTests(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_env = os.environ.copy()
        os.environ.clear()

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        os.environ.update(self.original_env)

    def test_env_file_loading(self):
        env_file_path = Path(self.test_dir) / ".env"
        env_file_path.write_text("DB_FILE=custom_name.sdb\n", encoding="utf-8")

        load_env_file(env_file_path)
        self.assertEqual(os.environ.get("DB_FILE"), "custom_name.sdb")

    def test_default_validation(self):
        env_file_path = Path(self.test_dir) / ".env"
        env_file_path.write_text("DB_FILE=custom_name.sdb\n", encoding="utf-8")

        config = Config.load(env_file_path)
        self.assertIsInstance(config.db_file, Path)
        self.assertEqual(str(config.db_file), "custom_name.sdb")

    def test_nested_directory_creation(self):
        nested_path = os.path.join(self.test_dir, "sub_folder", ".sdb")
        env_file_path = Path(self.test_dir) / ".env"
        env_file_path.write_text(f'DB_FILE="{nested_path}"\n', encoding="utf-8")

        config = Config.load(env_file_path)

        self.assertEqual(config.db_file, Path(nested_path))
        self.assertTrue(Path(self.test_dir, "sub_folder").exists())

    def test_permission_error_raise(self):
        nested_path = "/.sdb"
        env_file_path = Path(self.test_dir) / ".env"
        env_file_path.write_text(f'DB_FILE="{nested_path}"\n', encoding="utf-8")

        Config.load(env_file_path)
        self.assertRaises(PermissionError)
