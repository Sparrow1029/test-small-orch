from pathlib import Path
from orchestrator.settings import AppSettings as OrchCoreSettings


class AppSettings(OrchCoreSettings):
    SCRIPTS_DIR: Path = Path("/usr/src/app/scripts")


app_settings = AppSettings()
