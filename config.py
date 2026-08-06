import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

def load_json(filename: str) -> dict | list:
    path = DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Arquivo {filename} não encontrado em {DATA_DIR}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)