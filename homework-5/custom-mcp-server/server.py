from pathlib import Path

from fastmcp import FastMCP

mcp = FastMCP("lorem-reader")
LOREM_FILE = Path(__file__).with_name("lorem-ipsum.md")


def _word_limited_content(word_count: int = 30) -> str:
    if word_count <= 0:
        raise ValueError("word_count must be greater than 0")

    text = LOREM_FILE.read_text(encoding="utf-8")
    words = text.split()
    return " ".join(words[:word_count])


@mcp.resource("lorem://ipsum")
def lorem_default() -> str:
    return _word_limited_content(30)


@mcp.resource("lorem://ipsum/{word_count}")
def lorem_by_word_count(word_count: int = 30) -> str:
    return _word_limited_content(word_count)


@mcp.tool(name="read")
def read_tool(word_count: int = 30) -> str:
    return _word_limited_content(word_count)


if __name__ == "__main__":
    mcp.run()
