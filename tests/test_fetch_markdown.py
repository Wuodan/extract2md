from __future__ import annotations

import pytest

from fetch_markdown import Html2MarkdownError, fetch_to_markdown

HF_URL = "https://huggingface.co/unsloth/GLM-4.6-GGUF"


def test_fetch_to_markdown_huggingface(tmp_path) -> None:
    try:
        markdown = fetch_to_markdown(HF_URL)
    except Html2MarkdownError as exc:  # pragma: no cover - depends on network
        pytest.skip(f"Unable to contact Hugging Face: {exc}")

    output_path = tmp_path / "huggingface.md"
    output_path.write_text(markdown, encoding="utf-8")
    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8")
    assert markdown
    print(f"Markdown saved to {output_path}")
    assert "glm" in markdown.lower()
