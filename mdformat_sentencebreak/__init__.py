"""An mdformat plugin for..."""

from importlib.metadata import version

__version__ = version("mdformat_sentencebreak")

from .plugin import RENDERERS, update_mdit  # noqa: E402, F401
