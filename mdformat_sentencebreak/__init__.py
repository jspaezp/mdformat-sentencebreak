"""An mdformat plugin for..."""

import importlib.metadata

__version__ = importlib.metadata.version(__name__)

from .plugin import RENDERERS, update_mdit  # noqa: E402, F401
