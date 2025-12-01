import tomllib


from pathlib import Path

DEFAULT_CONFIG_PATH = Path(__file__).parent / "config.toml"


class OmiConfig:
    def __init__(self):
        self.data = {}
        if DEFAULT_CONFIG_PATH.exists():
            self.data = tomllib.loads(DEFAULT_CONFIG_PATH.read_text())

    def get(self, section: str, key: str, default=None):
        return self.data.get(section, {}).get(key, default)


CONFIG = OmiConfig()
