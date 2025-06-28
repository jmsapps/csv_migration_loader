from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()


def getenv(key: str, default: Optional[str] = None):
    return os.getenv(key, default)
