import os
from dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseModel
import base64

load_dotenv(dotenv_path=Path(".env"))

def is_authorized(auth_key: str) -> bool:
    envkey = os.getenv("KEY")
    expected_key = base64.b64encode(envkey.encode()).decode()
    return auth_key == expected_key