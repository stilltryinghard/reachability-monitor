import json
from pathlib import Path

BUFFER_FILE = Path("buffer.jsonl")
MAX_BUFFER = 1000  # Лимит, чтобы не расти бесконечно


def add(measurement: dict) -> None:
    """Дописать замер в буффер, соблюдая лимиты."""
    current = read_all()
    current.append(measurement)
    if len(current) > MAX_BUFFER:
        current = current[-MAX_BUFFER:]
    replace_all(current)
        
        
def read_all() -> list[dict]:
    """Прочитать все замеры из буфера"""
    if not BUFFER_FILE.exists():
        return []
    with open(BUFFER_FILE, "r") as f:
        return [json.loads(line) for line in f if line.strip()]
    

def replace_all(measurements: list[dict]) -> None:
    """Перезаписать буфер списком (недосланный хвост). Пустой список - очистить"""
    if not measurements:
        BUFFER_FILE.unlink(missing_ok=True)
        return
    with open(BUFFER_FILE, "w") as f:
        f.writelines(f"{json.dumps(m)}\n" for m in measurements)