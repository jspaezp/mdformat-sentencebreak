from pathlib import Path

from markdown_it.utils import read_fixture_file
import mdformat
import pytest

FIXTURE_PATH = Path(__file__).parent / "fixtures"


fixtures = []

for i in FIXTURE_PATH.glob("*.md"):
    fixtures.extend(read_fixture_file(i))


@pytest.mark.parametrize(
    "line,title,text,expected", fixtures, ids=[f[1] for f in fixtures]
)
def test_fixtures(line, title, text, expected):
    output = mdformat.text(text, extensions={"sentencebreak"})
    print(output)
    expected_lines = expected.rstrip().splitlines()
    output_lines = output.rstrip().splitlines()
    iterable = zip(expected_lines, output_lines, strict=True)
    iterable = enumerate(iterable)

    offset = line + len(text.splitlines()) + 2
    for i, (expect_line, out_line) in iterable:
        message = f"Line {i+offset}:\n {expect_line} != {out_line}\n in {title}"
        assert expect_line == out_line, message
