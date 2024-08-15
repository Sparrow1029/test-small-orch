from pathlib import Path
from orchestrator.settings import AppSettings as OrchCoreSettings
from oauth2_lib.settings import Oauth2LibSettings


class AppSettings(OrchCoreSettings):
    SCRIPTS_DIR: Path = Path("/usr/src/app/scripts")


app_settings = AppSettings()
