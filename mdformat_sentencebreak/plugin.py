import logging
import random
import re
from typing import Mapping

from markdown_it import MarkdownIt
from mdformat.renderer import RenderContext, RenderTreeNode
from mdformat.renderer._context import bullet_list, ordered_list
from mdformat.renderer.typing import Render


class PunctuationRegexes:
    CLOSING_PUNCTUATION = r"[\]}.,;:!?)\]+]"  # punctuations that denote closure
    BREAKS = (
        r"(?<=" + CLOSING_PUNCTUATION + r")\n+"
    )  # punctuation followed by newline(s), not matching punctuations
    CLOSING_PUNCTUATION = re.compile(CLOSING_PUNCTUATION)
    BREAKS = re.compile(BREAKS)
    # With positive lookbehind, finds closing punctuation that
    # is followed for at least 42 characters before the end of the line
    # matches as few characters as possible
    # TODO make this configurable
    # TODO make this a list an implement a 'search falling back'
    # so there are more levels of falling back
    SENTENCEBREAK_FALLBACK = re.compile(r"(?<=[}.,;:!?)]).{22,}?$")
    SENTENCEBREAK_IDEAL = re.compile(r"(?<=[.,;:!?]).{22,120}$")


def _next_sentencebreak(text):
    match = PunctuationRegexes.SENTENCEBREAK_IDEAL.search(text)
    if match is None:
        match = PunctuationRegexes.SENTENCEBREAK_FALLBACK.search(text)

    return match


def break_sentences(text: str):
    broken = re.compile(PunctuationRegexes.BREAKS).split(text)

    outs = []
    for sentence in broken:
        # TODO consider here wether to keep already broken sentences
        # or to remove newlines that are not preceeded by a closing punctuation
        sentence = sentence.strip().replace("\n", " ")
        partial_outs = []
        while len(sentence) > 42:
            match = _next_sentencebreak(sentence)
            if match is None:
                break

            chunk = sentence[match.span()[0] :].strip()
            partial_outs.append(chunk)
            sentence = sentence[: match.span()[0]].strip()

        [outs.append(x) for x in [sentence] + (partial_outs[::-1]) if x]

    return "\n".join(outs)


class PlaceholderMaker:
    placeholder_chars = "abcdefghijklmnopqrstuvwxyz"
    placeholder_chars += placeholder_chars.upper()

    def __init__(self, ignores=None):
        self.placeholders = {}
        self.counter = 0
        self.ignores = ignores or []

    def __call__(self, string):
        self.counter += 1
        ph = self._make_placeholder(string)
        return ph

    def _make_placeholder(self, string):
        length = len(string)
        attempts = 0
        while True:
            ph = self._random_placeholder(length)
            if ph not in self.placeholders and ph not in self.ignores:
                break
            attempts += 1
            if attempts > 100:
                raise ValueError(f"Could not find a unique placeholder for '{string}'")

        self.placeholders[ph] = string
        return ph

    @classmethod
    def _random_placeholder(cls, length):
        ph = "".join(random.choices(cls.placeholder_chars, k=length - 1)) + "]"
        return ph

    def __getitem__(self, key):
        return self.placeholders[key]

    def replace_placeholders(self, text):
        for ph, replacement in self.placeholders.items():
            text = text.replace(ph, replacement)
        return text


def update_mdit(mdit: MarkdownIt) -> None:
    """Update the parser, e.g. by adding a plugin: `mdit.use(myplugin)`"""
    mdit.enable("list")


def _render_paragraph(node: RenderTreeNode, context: RenderContext) -> str:
    """Render a `RenderTreeNode` of type "paragraph"."""

    assert len(node.children) == 1
    inline = node.children[0]

    outs = [child.render(context) for child in inline.children]
    phm = PlaceholderMaker("\n".join(outs))

    zips = zip(outs, inline.children)
    outs = [phm(x) if y.token is None else x for x, y in zips]
    outs = "".join(outs)

    out = break_sentences(outs)
    out = phm.replace_placeholders(out)
    logging.debug("Rendered paragraph: " + out)

    return out


def _list_item(node: RenderTreeNode, context: RenderContext) -> str:
    renders = [child.render(context) for child in node.children]
    out = ""

    for render, child in zip(renders, node.children):
        logging.debug(f"type: {child.type}")
        logging.debug("List item render: %s", render)

        if child.type != "paragraph":
            render = "\n" + render

        out += render
        logging.debug("List item out: %s", out)

    if not out.strip():
        return ""

    return out


RENDERERS: Mapping[str, Render] = {
    "bullet_list": bullet_list,
    "ordered_list": ordered_list,
    "paragraph": _render_paragraph,
    "list_item": _list_item,
}
