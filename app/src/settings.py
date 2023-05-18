from pathlib import Path


BASE_DIR: Path = Path(__file__).parent.parent.parent
APP_DIR: Path = BASE_DIR / 'app'
TEMP_DIR: Path = APP_DIR / 'temp'
DATA_DIR: Path = APP_DIR / 'data'
TEST_DIR: Path = BASE_DIR / 'tests'
DATA_AMOUNT_IN_DAYS: int = 30

if not TEMP_DIR.exists():
    TEMP_DIR.mkdir()

if not DATA_DIR.exists():
    DATA_DIR.mkdir()
