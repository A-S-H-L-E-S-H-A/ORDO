"""ORDO storage package."""

from .config import settings
from .db.base import Base

__all__ = ["Base", "settings"]
